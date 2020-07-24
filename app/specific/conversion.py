from __future__ import unicode_literals

import flask_sijax
from flask import Blueprint, request, send_file, flash, render_template, g

from app import basedir
from app.helpers.ConversionHelper import ConversionHelper
from app.helpers.YtSearch import YtSearch

conversion = Blueprint('conversion', __name__)


@conversion.route('/convertMp3', methods=['POST'])
def convert_mp3():

    url = request.form.get('url')

    render_template('main.html')
    # make conversion
    filename = ConversionHelper(url).process_conversion()

    render_template('main.html')
    # directory things
    directory = basedir+'/downloads/'
    filename = filename+'.mp3'

    # set download name
    final_title = request.form.get('title')+'.mp3' if request.form.get('title') else filename

    render_template('main.html')

    # return song to user
    return send_file(directory+filename, attachment_filename=final_title, as_attachment=True)


@conversion.route('/convertItemMp3', methods=['GET'])
def convert_item_mp3():

    video_id = request.args.get('video_id', type=str)

    url = 'https://www.youtube.com/watch?v='+video_id

    flash('Conversion starting')
    render_template('main.html')
    # make conversion
    filename = ConversionHelper(url).process_conversion()

    flash('Conversion ended ... a sec please')
    render_template('main.html')
    # directory things
    directory = basedir+'/downloads/'
    filename = filename+'.mp3'

    # set download name
    final_title = request.form.get('title')+'.mp3' if request.form.get('title') else filename

    flash('Conversion completed!')
    render_template('main.html')

    # return song to user
    return send_file(directory+filename, attachment_filename=final_title, as_attachment=True)


@flask_sijax.route(conversion, "/searchyt", methods=['GET', 'POST'])
def youtube_search():

    def search_results(obj_response, search_str):
        yt_results = YtSearch(search_str, "EN").perform_search()
        obj_response.call(yt_results)

    # def goodbye_handler(obj_response):
    #     obj_response.alert('Goodbye, whoever you are.')
    #     obj_response.html('#yolo', '<p>fuck you</p>')

    if g.sijax.is_sijax_request:
        g.sijax.register_callback('search_results', search_results)
        return g.sijax.process_request()

    return render_template('main.html')
