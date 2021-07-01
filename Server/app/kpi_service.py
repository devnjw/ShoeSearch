from flask import render_template, jsonify, make_response, request
from flask_restful import Resource, abort

from app import db
from app.models import KPI, SearchKeywords

from datetime import datetime, timedelta

def add_num_visit_home():
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        kpi = KPI.query.filter_by(date=today).first()
        if not kpi:
            kpi = KPI(
                date = today,
                visit = 1,
                string_search = 0,
                image_search = 0
            )
            db.session.add(kpi)
            db.session.commit()
        else:
            kpi.visit += 1
            db.session.commit()
    except Exception as e:
        print(e)

def add_num_string_search():
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        kpi = KPI.query.filter_by(date=today).first()
        if not kpi:
            kpi = KPI(
                date = today,
                visit = 0,
                string_search = 1,
                image_search = 0
            )
            db.session.add(kpi)
            db.session.commit()
        else:
            kpi.string_search += 1
            db.session.commit()
    except Exception as e:
        print(e)

def add_num_image_search():
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        kpi = KPI.query.filter_by(date=today).first()
        if not kpi:
            kpi = KPI(
                date = today,
                visit = 0,
                string_search = 0,
                image_search = 1
            )
            db.session.add(kpi)
            db.session.commit()
        else:
            kpi.image_search += 1
            db.session.commit()
    except Exception as e:
        print(e)

def add_search_keyword_log(keyword):
    try:
        today = datetime.today().strftime('%Y-%m-%d')
        seach_log = SearchKeywords.query.filter_by(date=today, keyword=keyword).first()
        if not seach_log:
            seach_log = SearchKeywords(
                date = today,
                keyword = keyword,
                cnt = 1
            )
            db.session.add(seach_log)
            db.session.commit()
        else:
            seach_log.cnt += 1
            db.session.commit()
    except Exception as e:
        print(e)