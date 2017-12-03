# coding = utf-8
from flask import Blueprint, render_template
from flask import request, current_app
from jobplus.models import db, User, Job, Company, Status


front = Blueprint('front', __name__)


@front.route('/')
def index():
    page = request.args.get('page', default=1, type=int)
    pagination = Job.query.paginate(
        page=page,
        per_page=current_app.config['INDEX_PRE_PAGE'],
        error_out=False
    )
    return render_template('index.html', pagination=pagination)