import obspython as obs
import urllib.request
import urllib.error

from time import sleep

starturl         = ""
stopurl          = ""
enable_rec       = False
enable_stream    = False

interval = 1

curRec    = False
curStream = False

# ------------------------------------------------------------

def load_url(url):
    try:
        urllib.request.urlopen(url)

    except urllib.error.URLError as err:
        obs.script_log(obs.LOG_WARNING, "Error opening URL '" + url + "': " + err.reason)
        
def load_start_url():
    global starturl
    obs.script_log(obs.LOG_DEBUG, "Trying to start...")
    
    if starturl != "":
        obs.script_log(obs.LOG_DEBUG, "Accessing Start URL")
        load_url(starturl)

def load_stop_url():
    global stopurl
    obs.script_log(obs.LOG_DEBUG, "Trying to stop...")

    if stopurl != "":
        obs.script_log(obs.LOG_DEBUG, "Accessing Stop URL")
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
    global enable_rec
    global enable_stream
    
    is_streaming = curStream
    is_recording = curRec
    
    obs.script_log(obs.LOG_DEBUG, "Got 'Start' Signal")
    obs.script_log(obs.LOG_DEBUG, "Streaming? "+str(is_streaming)+" Recording? "+str(is_recording))
    obs.script_log(obs.LOG_DEBUG, "Streaming enabled? "+str(enable_stream)+" Recording Enabled? "+str(enable_rec))

    if (is_streaming and enable_stream) or (is_recording and enable_rec):
        load_start_url()
    
def load_stop_url_cb():
    global curRec
    global curStream
    global enable_rec
    global enable_stream
    
    is_streaming = curStream
    is_recording = curRec

    obs.script_log(obs.LOG_DEBUG, "Got 'Stop' Signal")

    obs.script_log(obs.LOG_DEBUG, "Streaming? "+str(is_streaming)+" Recording? "+str(is_recording))
    obs.script_log(obs.LOG_DEBUG, "Streaming enabled? "+str(enable_stream)+" Recording Enabled? "+str(enable_rec))

    disable = True

    if (is_streaming and enable_stream):
        disable = False

    if (is_recording and enable_rec):
        disable = False

    if disable:
        load_stop_url()
        
def check_stream_state():
    global curRec
    global curStream
    global enable_rec
    global enable_stream

    changed=False
    
    stream_active = obs.obs_frontend_streaming_active()
    rec_active    = obs.obs_frontend_recording_active()

    if enable_rec and (rec_active != curRec):
        changed = True

    if enable_stream and (stream_active != curStream):
        changed = True

    if changed:
        light_on = False

        if enable_rec and rec_active:
            light_on = True
            
        if enable_stream and stream_active:
            light_on = True

        if light_on:
            load_start_url()
        else:
            load_stop_url()

    curStream = stream_active
    curRec = rec_active

# ------------------------------------------------------------

def script_description():
    return "Accesses a URL when streaming starts and another when streaming stops.  Intended for use with a recording light.\n\nBy TheAstropath"

def script_update(settings):
    global starturl
    global stopurl
    global enable_rec
    global enable_stream
    global interval

    starturl        = obs.obs_data_get_string(settings, "starturl")
    stopurl         = obs.obs_data_get_string(settings, "stopurl")

    enable_rec      = obs.obs_data_get_bool(settings,"enablerec")
    enable_stream   = obs.obs_data_get_bool(settings,"enablestream")

    interval        = obs.obs_data_get_int(settings,"interval")

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

def register_callbacks():
    register_output_stream_callbacks("simple_stream")
    register_output_stream_callbacks("adv_stream")
    register_output_stream_callbacks("ffmpeg_output")
    register_output_rec_callbacks("simple_file_output")
    register_output_rec_callbacks("adv_file_output")
    register_output_rec_callbacks("adv_ffmpeg_output")    

def remove_callbacks():
    remove_output_stream_callbacks("simple_stream")
    remove_output_stream_callbacks("adv_stream")
    remove_output_stream_callbacks("ffmpeg_output")
    remove_output_rec_callbacks("simple_file_output")
    remove_output_rec_callbacks("adv_file_output")
    remove_output_rec_callbacks("adv_ffmpeg_output")    

def ensure_callbacks_in_place():
    remove_callbacks()
    register_callbacks()

def script_load(settings):
    global curRec
    global curStream
    obs.script_log(obs.LOG_DEBUG, "Loading script")
    curStream = obs.obs_frontend_streaming_active()
    curRec    = obs.obs_frontend_recording_active()

    obs.timer_add(check_stream_state,1000)
    
    #register_callbacks()

def script_unload():
    obs.script_log(obs.LOG_DEBUG, "Unloading script")
    obs.timer_remove(check_stream_state)
    
    #remove_callbacks()


def script_defaults(settings):
    global interval
    interval = 1

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "starturl", "Start URL", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "stopurl", "Stop URL", obs.OBS_TEXT_DEFAULT)

    obs.obs_properties_add_bool(props,"enablerec","Enable for Recording")
    obs.obs_properties_add_bool(props,"enablestream","Enable for Streaming")

    obs.obs_properties_add_button(props, "startbutton", "Test Start URL", test_start_url)
    obs.obs_properties_add_button(props, "stopbutton", "Test Stop URL", test_stop_url)

    obs.obs_properties_add_int(props,"interval","Check Interval",1,60,1)
    
    return props
