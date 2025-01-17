from flask import Blueprint, request, jsonify
from app.models import *
from app import engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import unquote
from datetime import datetime


polls = Blueprint('polls', __name__)
PAGE_SIZE = 6


@polls.route('/polls/create', methods=['POST'])
def create_polls():
    # Authorization Here
    # TODO: Add authorization here
    # TODO: Add user_id when authorization is added

    user_id = 1
    title = request.json.get('title')
    count = request.json.get('count')
    create_time = request.json.get('create_time')
    expiration_time = request.json.get('expiration_time')
    expiration_time = expiration_time if expiration_time != '' else None
    sections = request.json.get('sections')

    try:
        Session = sessionmaker(bind=engine)
        session = Session()

        expiration_time = datetime.strptime(expiration_time, '%Y-%m-%d %H:%M:%S')
        create_time = datetime.strptime(create_time, '%Y-%m-%d %H:%M:%S')

        poll = Polls(
            user_id=user_id,
            title=title,
            count=count,
            create_time=create_time,
            expiration_time=expiration_time
        )
        session.add(poll)
        session.commit()

        for section in sections:
            new_section = Section(
                poll_id=poll.get_id(),
                title=section['title'],
                description=section['description'],
                order_value=section['order_value']
            )
            session.add(new_section)
            session.commit()

            for vote in session['votes']:
                new_vote = Votes(
                    section_id=new_section.get_id(),
                    title=vote['title'],
                    vote_type=vote['type'],
                    limit_count=vote['limit_count'],
                    order_value=vote['order_value']
                )
                session.add(new_vote)
                session.commit()

                for choice in vote['choices']:
                    new_choice = Choices(
                        vote_id=new_vote.get_id(),
                        description=choice['description'],
                        choice_type=choice['type']
                    )
                    session.add(new_choice)
                session.commit()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Failed', 'error': str(e)})
    finally:
        return jsonify({'msg': 'Success'})


@polls.route('/polls/getList', methods=['GET'])
def getList():
    # TODO: Add authorization to get user_id
    user_id = 1

    collection = request.args.get('collection')
    keywords = unquote(request.args.get('keywords'))
    keywords = keywords.split(' ') if keywords != '' else []
    sortBy = request.args.get('sortBy')
    published = request.args.get('published') or 'all'
    page = request.args.get('page') or 1
    page = int(page) if page != '' else 1


    if collection == 'star':
        star_polls = StarList.query.filter_by(user_id=int(user_id)).all()
        polls = [Polls.query.filter_by(id=star.poll_id).first() for star in star_polls]
    elif collection == 'deleted':
        polls = Polls.query.filter_by(user_id=int(user_id), status=2).all()
    else:
        polls = Polls.query.filter_by(user_id=int(user_id)).all()


    if published != 'all':
        status = 1 if published == 'true' else 0
        polls = list(filter(lambda x: x.status == status, polls))


    if len(keywords) > 0:
        polls = list(filter(lambda x: any([keyword in x.title for keyword in keywords]), polls))


    if sortBy == 'timeAsc':
        polls = sorted(polls, key=lambda x: x.create_time)
    elif sortBy == 'timeDesc':
        polls = sorted(polls, key=lambda x: x.create_time, reverse=True)
    elif sortBy == 'countAsc':
        polls = sorted(polls, key=lambda x: x.count)
    elif sortBy == 'countDesc':
        polls = sorted(polls, key=lambda x: x.count, reverse=True)


    polls = list(polls)
    pages = len(polls) + (PAGE_SIZE - 1) // PAGE_SIZE
    polls = polls[(page - 1) * PAGE_SIZE: min(page * PAGE_SIZE, len(polls))]

    return jsonify({
        'status': '200',
        'msg': 'Success',
        'paging': {'current': page, 'total': pages},
        'data': [{
            'id': poll.id,
            'title': poll.title,
            'status': poll.status,
            'isStared': StarList.query.filter_by(user_id=user_id, poll_id=poll.id).first() is not None,
            'count': poll.count,
            'public_time': poll.public_time.strftime('%Y-%m-%d %H:%M:%S') if poll.public_time is not None else None,
            'create_time': poll.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            'expiration_time': poll.expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
        } for poll in polls]
    })


@polls.route('/polls/<int:poll_id>', methods=['GET'])
def get_poll(poll_id):
    poll = Polls.query.filter_by(id=poll_id).first()
    sections = Section.query.filter_by(poll_id=poll_id).all()

    # TODO: Add authorization to getting poll

    try:
        response = {
            'id': poll.id,
            'title': poll.title,
            'count': poll.count,
            # 'create_time': poll.create_time.strftime('%Y-%m-%d %H:%M:%S'),
            # 'expiration_time': poll.expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
            sections: [{
                'id': section.id,
                'poll_id': section.poll_id,
                'title': section.title,
                'description': section.description,
                'order_value': section.order_value,
                'votes': [{
                    'id': vote.id,
                    'section_id': vote.section_id,
                    'title': vote.title,
                    'vote_type': vote.vote_type,
                    'limit_count': vote.limit_count,
                    'order_value': vote.order_value,
                    'choices': [{
                        'id': choice.id,
                        'vote_id': choice.vote_id,
                        'description': choice.description,
                        'choice_type': choice.choice_type
                    } for choice in Choices.query.filter_by(vote_id=vote.id).all()]
                } for vote in Votes.query.filter_by(section_id=section.id).all()]
            } for section in sections]
        }
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Failed', 'error': str(e)})

    return jsonify(response)


@polls.route('/polls/polls/submitPoll', methods=['POST'])
def submit_poll():
    # TODO: Add authorization to get user_id
    user_id = 1

    poll_id = request.json.get('id')
    poll = Polls.query.filter_by(id=poll_id).first()

    if poll is None or poll.status == 0:
        return jsonify({'msg': 'Failed', 'error': 'Poll does not exist or is not published'})

    sections = request.json.get('sections')
    for section in sections:
        # assert Section.query.filter_by(id=section['id']).first() is not None
        for vote in section['votes']:
            # assert Votes.query.filter_by(id=vote['id']).first() is not None
            limit_count = Votes.query.filter_by(id=vote['id']).first().limit_count
            chosen_choice = filter(lambda x: x['isChoosed'].lower() == 'true', vote['choices'])

            if len(chosen_choice) > limit_count:
                return jsonify({'msg': 'Failed', 'error': 'Too many choices'})

            for choice in chosen_choice:
                new_choice = UserChoice(
                    user_id=user_id,
                    choice_id=choice['id'],
                    comment=choice['comment'],
                    order_value=choice['orderValue'],
                    is_choosed=True
                )
                db.session.add(new_choice)
                db.session.commit()
                update_vote_count(choice['id'])

            unchosen_choice = filter(lambda x: x['isChoosed'].lower() == 'false', vote['choices'])
            for choice in unchosen_choice:
                new_choice = UserChoice(
                    user_id=user_id,
                    choice_id=choice['id'],
                    comment=choice['comment'],
                    order_value=choice['orderValue'],
                    is_choosed=False
                )
                db.session.add(new_choice)
                db.session.commit()
                delete_vote_count(choice['id'])

    return jsonify({'msg': 'Success'})


@polls.route('/polls/getAnalysisData/<int:poll_id>', methods=['GET'])
def get_analysis_data(poll_id):
    poll = Polls.query.filter_by(id=poll_id).first()
    if poll is None:
        return jsonify({'msg': 'Failed', 'error': 'Poll does not exist'})

    sections = Section.query.filter_by(poll_id=poll_id).all()
    votes = Votes.query.filter(Votes.section_id.in_([section.id for section in sections])).all()

    average = lambda x: sum(x) / len(x) if len(x) > 0 else 0

    return jsonify({
        'id': poll.id,
        'title': poll.title,
        'count': poll.count,
        'user': {'id': poll.user_id, 'name': poll.user.name},
        'create_time': poll.create_time.strftime('%Y-%m-%d %H:%M:%S'),
        'public_time': poll.public_time.strftime('%Y-%m-%d %H:%M:%S') if poll.public_time is not None else None,
        'expiration_time': poll.expiration_time.strftime('%Y-%m-%d %H:%M:%S'),
        'votes': [{
            'id': vote.id,
            'title': vote.title,
            'type': vote.vote_type,
            'limitCount': vote.limit_count,
            'choiceResults': [{
                'description': choice.description,
                'count': VoteCount.query.filter_by(id=choice.id).first().cnt,
                'score': vote.vote_type == 4 and average(
                    [user_choice.order_value for user_choice in UserChoice.query.filter_by(choice_id=choice.id).all()]) or 0,
                'comments': [user_choice.comment for user_choice in UserChoice.query.filter_by(choice_id=choice.id).all()]
            } for choice in Choices.query.filter_by(vote_id=vote.id).all()]
        } for vote in votes]
    })


@polls.route('/polls/changePublishStatus/<int:poll_id>', methods=['POST'])
def change_publish_status(poll_id):
    # TODO: Add authorization to check privilege

    poll = Polls.query.filter_by(id=poll_id).first()
    if poll is None:
        return jsonify({'msg': 'Failed', 'error': 'Poll does not exist'})

    try:
        if poll.status == 0:
            poll.status = 1
            poll.public_time = datetime.strptime(request.json.get('public_time'), '%Y-%m-%d %H:%M:%S')
        elif poll.status == 1:
            poll.status = 0
            poll.public_time = None
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Failed', 'error': str(e)})
    return jsonify({'msg': 'Success', 'status': poll.status})


@polls.route('/polls/collect/<int:poll_id>', methods=['POST'])
def collect(poll_id):
    # TODO: Add authorization to get user_id
    user_id = 1

    try:
        star = StarList.query.filter_by(user_id=user_id, poll_id=poll_id).first()
        if star is not None:
            db.session.delete(star)
            return jsonify({'msg': 'Unstar success'})

        new_star = StarList(user_id=user_id, poll_id=poll_id)
        db.session.add(new_star)
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Failed', 'error': str(e)})
    return jsonify({'msg': 'Star success'})


@polls.route('/polls/copy/<int:poll_id>', methods=['GET'])
def collect_list(poll_id):
    # TODO: Add authorization to get user_id
    user_id = 1
    
    poll = Polls.query.filter_by(id=poll_id).first()
    if poll is None:
        return jsonify({'msg': 'Failed', 'error': 'Poll does not exist'})

    try:
        new_poll = Polls(
            user_id=user_id,
            title=poll.title,
            count=poll.count,
            create_time=poll.create_time,
            expiration_time=poll.expiration_time
        )
        db.session.add(new_poll)
        db.session.commit()

        sections = Section.query.filter_by(poll_id=poll_id).all()
        for section in sections:
            new_section = Section(
                poll_id=new_poll.get_id(),
                title=section.title,
                description=section.description,
                order_value=section.order_value
            )
            db.session.add(new_section)
            db.session.commit()

            votes = Votes.query.filter_by(section_id=section.id).all()
            for vote in votes:
                new_vote = Votes(
                    section_id=new_section.get_id(),
                    title=vote.title,
                    vote_type=vote.vote_type,
                    limit_count=vote.limit_count,
                    order_value=vote.order_value
                )
                db.session.add(new_vote)
                db.session.commit()

                choices = Choices.query.filter_by(vote_id=vote.id).all()
                for choice in choices:
                    new_choice = Choices(
                        vote_id=new_vote.get_id(),
                        description=choice.description,
                        choice_type=choice.choice_type
                    )
                    db.session.add(new_choice)
                db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Failed', 'error': str(e)})
    return jsonify({'msg': 'Success'})


@polls.route('/polls/delete/<int:poll_id>', methods=['POST'])
def delete(poll_id):
    # TODO: Add privilege check

    if poll_id == 0:
        return jsonify({'msg': 'Success'})

    poll = Polls.query.filter_by(id=poll_id).first()
    if poll is None:
        return jsonify({'msg': 'Failed', 'error': 'Poll does not exist'})

    updated = request.args.get('updated').startswith('true')

    try:
        if updated or poll.status == 2:
            db.session.delete(poll)
        else:
            poll.status = 2
        db.session.commit()
    except Exception as e:
        print(e)
        return jsonify({'msg': 'Failed', 'error': str(e)})
    return jsonify({'msg': 'Success'})


# Trigger functions
def update_vote_count(choice_id):
    try:
        choice = VoteCount.query.filter_by(id=choice_id).first()
        if choice is None:
            choice = VoteCount(choice_id=choice_id, cnt=0)
        choice.cnt += 1
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False

def delete_vote_count(choice_id):
    try:
        choice = VoteCount.query.filter_by(id=choice_id).first()
        if choice is None or choice.cnt == 0:
            return True

        choice.cnt -= 1
        db.session.commit()
        return True
    except Exception as e:
        print(e)
        return False
