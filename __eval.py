#!/Users/jye/.brew/bin/python3
import os
import requests as req
import sys
from random import random
from getopt import gnu_getopt
from datetime import datetime as dt
from datetime import date
from datetime import timezone as tz
from datetime import timedelta as td
from datetime import time
from time import sleep
from html.parser import HTMLParser


#### CONTEXT evaluation when selecting a slot
    # var _this2 = this;

    # var $list = this._$modal.find('.modal-body select');
    # var indexSelectedId = $list.val() >> 0;
    # var ids = $list.data('ids').split(",").slice(indexSelectedId, indexSelectedId + this._$calendar.data('duration')).join(',');
    # var url = this._$calendar.data('update-url').replace(':ids', ids);

    # this._waitingAjax = true;
    # this._$loading.show();
    # this._$modal.find('.btn-primary').addClass('disable');
    # _jquery2.default.ajax({
    #     url: url,
    #     type: 'post',
    #     dataType: 'json',
    #     data: {
    #         'start': this._$calendar.fullCalendar('getView').start.format(),
    #         'end': this._$calendar.fullCalendar('getView').end.format(),
    #         '_method': "put"
    #     }


#### CONTEXT when logging in    
    ## rails-on-ruby backend
    ## below is parameter parsing
    # utf8=✓&authenticity_token={token}&user[login]={user}&user[password]={passwd}&commit=Sign+in
    ## needs also in header
    ##
    # Host: signin.intra.42.fr
    # User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:66.0) Gecko/20100101 Firefox/66.0
    # Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    # Accept-Language: en-US,en;q=0.5
    # Accept-Encoding: gzip, deflate, br
    # Referer: https://signin.intra.42.fr/users/sign_in
    # Content-Type: application/x-www-form-urlencoded
    # Content-Length: 199
    # DNT: 1
    # Connection: keep-alive
    # Cookie: _intra_42_session_production=efb9b0603f4fbce5c0a65cf1bc106ecb
    # Upgrade-Insecure-Requests: 1

class CSRF_sniffer(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag == "meta" and attrs[0] == ('name', 'csrf-token'):
            self._token = attrs[1][1]
        elif tag == "div" and 'data-duration' in attrs[0]:
            self._duration = attrs[0][1]

    def get_csrf_token(self):
        return self._token

    def get_duration(self):
        return self._duration

ENTRY_POINT ={
    "csrf": "https://projects.intra.42.fr/projects/{project}/slots",
    "get_slot":"https://projects.intra.42.fr/projects/{project}/slots.json?start={s}&end={e}",
    "select_slot":"https://projects.intra.42.fr/projects/{project}/slots/{ids}.json"
}

def _request(method:str, target:str,
             data:dict=None, headers:dict=None):
    prep = req.Request(method, target, data=data, headers=headers).prepare()
    # sign = hmac.new(secret, bytes(prep.body, 'utf-8'), digestmod=hashlib.sha256)
    # prep.body += '&signature=' + sign.hexdigest()
    # prep.url += '?' + prep.body
    with req.Session() as ses:
        ans = ses.send(prep)
    ans.raise_for_status()
    return ans

def _next_available(_min:time, _max:time, selected:list = []):
    _t = _min
    _time = _min.minute
    _t = time(_t.hour, 0)
    while _min < _max:
        _min = time(
            _t.hour + int(_time / 60),
            _t.minute + (_time % 60))
        if _min not in selected:
            yield _min
        _time += 15

def _iter_time(interval:int, iteration:int, _time:time):
    _int = _time.minute
    _time = time(_time.hour, 0)
    for x in range(0, iteration):
        yield time(
            _time.hour + int(_int / 60),
            _time.minute + (_int % 60))
        _int += interval

class auto_slot:
    def __init__(self, session:str, projects:list):
        ## projects to check
        ## and session id to use
        self._session = session
        self._projects = projects
        ## tick
        self._tick = 4
        self._sleep = 60 / self._tick
        ## the range
        _ctime = dt.now(tz(td(hours=2))) + td(days=1)
        self._start = _ctime.date()
        self._end = (_ctime+td(days=14)).date()
        print(self._start, self._end)
        ## the moment of evalution to pick
        self._min_clock = time(15,00)
        self._max_clock = time(22,00)
        ## init variable
        self.__busy_time = []
        
    def loop(self):
        while self._projects:
            for x in self._projects:
                try:
                    ## if 403, means either the project cannot sub any more evaluation or ????
                    ans = _request("GET", ENTRY_POINT["get_slot"].format(project=x, s=self._start, e=self._end),
                                   headers={"Cookie": "_intra_42_session_production={session}".format(session=self._session)}).json()
                except requests.exceptions.HTTPError as err:
                    ## if errored, remove the project
                    self._projects.remove(x)
                    continue

                print(ans)
                print(x)
                ## sniff csrf token, and duration
                z = CSRF_sniffer()
                z.feed(_request("GET", ENTRY_POINT['csrf'].format(project=x),
                                headers={"Cookie": "_intra_42_session_production={session}".format(session=self._session)}).text)
                duration = int(z.get_duration())
                print(z.get_csrf_token(), duration)

                ## check all interval
                for _eval in ans:
                    _eval_dts = dt.strptime(_eval["start"], '%Y-%m-%dT%H:%M:%S.%f%z')
                    print("start:", _eval_dts)
                    _eval_s = _eval_dts.time()
                    _eval_dte = (dt.strptime(_eval["end"], '%Y-%m-%dT%H:%M:%S.%f%z') - td(minutes=duration*15))
                    print("end:", _eval_dte)
                    _eval_e = _eval_dte.time()
                    _eval_ids = _eval["ids"].split(",")
                    print("ids:", _eval_ids)
                    ## make generator for available time and the evaluation,
                    __iter_avail = [x for x in _next_available(self._min_clock, self._max_clock, self.__busy_time)]
                    print("__iter_avail:", __iter_avail)
                    __iter_eval = [x for x in _next_available(_eval_s, _eval_e)]
                    print("__iter_eval:", __iter_eval)
                    for t in __iter_eval:
                        if t in __iter_avail:
                            ## make the interval unavailable
                            self.__busy_time += _iter_time(15, duration, t)
                            idx_ids = __iter_eval.index(t)
                            if idx_ids == -1:
                                raise ValueError
                            _s = (_eval_dts - td(days=_eval_dts.weekday())).date()
                            _e = (_s + td(days=6))
                            print(str(_s), str(_e))
                            ## push the request, emulate a little the header, but they can still track you down with sessionID
                            _request("POST", ENTRY_POINT["select_slot"].format(project=x, ids=",".join(_eval_ids[idx_ids:idx_ids+duration-1])),
                                     headers={"Cookie": "_intra_42_session_production={session}".format(session=self._session),
                                              "X-CSRF-Token": z.get_csrf_token(),
                                              "X-Requested-With": "XMLHttpRequest",
                                              "Agent-User": "ur.mom.v1",
                                              "Accept": "*/*",
                                              "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                                              "Referer": ENTRY_POINT['csrf'].format(project=x)
                                     },
                                     data={'start': str(_s), 'end': str(_e), '_method': 'put'})
                            break
                ## sleep between project request, interval should be random so it doesn't seem like a bot
                sleep(random()*2)
            ## for each iteration of project sleep.
            sleep(self._sleep)
            ## reset busy_time 
            if dt.now(tz(td(hours=2))).time() >= self._max_clock:
                self.__reset()

    def __reset(self):
        self.__busy_time.clear()
        _ctime = dt.now(tz(td(hours=2))) + td(days=1)
        self._start = _ctime.date()
        self._end = (_ctime+td(days=14)).date()

if __name__ == "__main__":
    z = auto_slot("753ff96c3268aa4f17f0a75eebc5c12f", ["get_next_line"])
    z.loop()
