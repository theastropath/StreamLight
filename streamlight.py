import obspython as obs
import urllib.request
import urllib.error

from time import sleep

starturl         = ""
stopurl          = ""
enable_rec       = False
enable_stream    = False

curRec    = False
curStream = False

# ------------------------------------------------------------

def load_url(url):
    try:
        urllib.request.urlopen(url)

    except urllib.error.URLError as err:
        obs.script_log(obs.LOG_WARNING, "Error opening URL '" + url + "': " + err.reason)
        
def load_start_url():
    if starturl != "":
        load_url(starturl)

def load_stop_url():
    if stopurl != "":
        load_url(stopurl)
        
def test_start_url(props, prop):
    load_start_url()
    
def test_stop_url(props, prop):
    load_stop_url()

def load_start_url_reccb(prop):
    global curRec
    curRec = True
    load_start_url_cb()

def load_stop_url_reccb(prop):
    global curRec
    curRec = False
    load_stop_url_cb()

def load_start_url_streamcb(prop):
    global curStream
    curStream = True
    load_start_url_cb()

def load_stop_url_streamcb(prop):
    global curStream
    curStream = False
    load_stop_url_cb()
    
    
def load_start_url_cb():
    global curRec
    global curStream
    
    is_streaming = curStream
    is_recording = curRec

    #obs.script_log(obs.LOG_WARNING, "Streaming? "+str(is_streaming)+" Recording? "+str(is_recording))
    #obs.script_log(obs.LOG_WARNING, "Streaming enabled? "+str(enable_stream)+" Recording Enabled? "+str(enable_rec))

    if (is_streaming and enable_stream) or (is_recording and enable_rec):
        load_start_url()
    
def load_stop_url_cb():
    global curRec
    global curStream
    
    is_streaming = curStream
    is_recording = curRec
    
    #obs.script_log(obs.LOG_WARNING, "Streaming? "+str(is_streaming)+" Recording? "+str(is_recording))
    #obs.script_log(obs.LOG_WARNING, "Streaming enabled? "+str(enable_stream)+" Recording Enabled? "+str(enable_rec))

    disable = True

    if (is_streaming and enable_stream):
        disable = False

    if (is_recording and enable_rec):
        disable = False

    if disable:
        load_stop_url()
        


# ------------------------------------------------------------

def script_description():
    return "Accesses a URL when streaming starts and another when streaming stops.  Intended for use with a recording light.\n\nBy TheAstropath"

def script_update(settings):
    global starturl
    global stopurl
    global enable_rec
    global enable_stream

    starturl        = obs.obs_data_get_string(settings, "starturl")
    stopurl         = obs.obs_data_get_string(settings, "stopurl")

    enable_rec      = obs.obs_data_get_bool(settings,"enablerec")
    enable_stream   = obs.obs_data_get_bool(settings,"enablestream")

def register_output_stream_callbacks(output_name):
    output = obs.obs_get_output_by_name(output_name)
    signal_handler = obs.obs_output_get_signal_handler(output)
    obs.signal_handler_connect(signal_handler,"start",load_start_url_streamcb)
    obs.signal_handler_connect(signal_handler,"stop",load_stop_url_streamcb)
    obs.obs_output_release(output)
    
def remove_output_stream_callbacks(output_name):
    output = obs.obs_get_output_by_name(output_name)
    signal_handler = obs.obs_output_get_signal_handler(output)
    obs.signal_handler_disconnect(signal_handler,"start",load_start_url_streamcb)
    obs.signal_handler_disconnect(signal_handler,"stop",load_stop_url_streamcb)
    obs.obs_output_release(output)

def register_output_rec_callbacks(output_name):
    output = obs.obs_get_output_by_name(output_name)
    signal_handler = obs.obs_output_get_signal_handler(output)
    obs.signal_handler_connect(signal_handler,"start",load_start_url_reccb)
    obs.signal_handler_connect(signal_handler,"stop",load_stop_url_reccb)
    obs.obs_output_release(output)
    
def remove_output_rec_callbacks(output_name):
    output = obs.obs_get_output_by_name(output_name)
    signal_handler = obs.obs_output_get_signal_handler(output)
    obs.signal_handler_disconnect(signal_handler,"start",load_start_url_reccb)
    obs.signal_handler_disconnect(signal_handler,"stop",load_stop_url_reccb)
    obs.obs_output_release(output)

def script_load(settings):
    global curRec
    global curStream

    curStream = obs.obs_frontend_streaming_active()
    curRec    = obs.obs_frontend_recording_active()
    
    register_output_stream_callbacks("simple_stream")
    register_output_stream_callbacks("adv_stream")
    register_output_stream_callbacks("ffmpeg_output")
    register_output_rec_callbacks("simple_file_output")
    register_output_rec_callbacks("adv_file_output")
    register_output_rec_callbacks("adv_ffmpeg_output")

def script_unload():
    remove_output_stream_callbacks("simple_stream")
    remove_output_stream_callbacks("adv_stream")
    remove_output_stream_callbacks("ffmpeg_output")
    remove_output_rec_callbacks("simple_file_output")
    remove_output_rec_callbacks("adv_file_output")
    remove_output_rec_callbacks("adv_ffmpeg_output")


def script_defaults(settings):
    pass

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "starturl", "Start URL", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "stopurl", "Stop URL", obs.OBS_TEXT_DEFAULT)

    obs.obs_properties_add_bool(props,"enablerec","Enable for Recording")
    obs.obs_properties_add_bool(props,"enablestream","Enable for Streaming")

    obs.obs_properties_add_button(props, "startbutton", "Test Start URL", test_start_url)
    obs.obs_properties_add_button(props, "stopbutton", "Test Stop URL", test_stop_url)
    return props
