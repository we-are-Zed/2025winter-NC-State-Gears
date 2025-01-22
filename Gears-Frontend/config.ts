import axios from "axios";

export const host = 'https://apifoxmock.com/m1/5015527-4675128-default';
// export const host ='https://vote.sustech.edu.cn'

export function createConnection() {
  return axios.create({
    baseURL: host,
    timeout: 10000
  });
}
