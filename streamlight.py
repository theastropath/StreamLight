import obspython as obs
import urllib.request
import urllib.error

starturl         = ""
stopurl          = ""

# ------------------------------------------------------------

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
    
def load_start_url_cb(prop):
    load_start_url()
    
def load_stop_url_cb(prop):
    load_stop_url()
    
def load_url(url):
    try:
        urllib.request.urlopen(url)

    except urllib.error.URLError as err:
        obs.script_log(obs.LOG_WARNING, "Error opening URL '" + url + "': " + err.reason)
        obs.remove_current_callback()

# ------------------------------------------------------------

def script_description():
    return "Accesses a URL when streaming starts and another when streaming stops.  Intended for use with a recording light.\n\nBy TheAstropath"

def script_update(settings):
    global starturl
    global stopurl

    starturl         = obs.obs_data_get_string(settings, "starturl")
    stopurl         = obs.obs_data_get_string(settings, "stopurl")

def register_output_callbacks(output_name):
    output = obs.obs_get_output_by_name(output_name)
    signal_handler = obs.obs_output_get_signal_handler(output)
    obs.signal_handler_connect(signal_handler,"start",load_start_url_cb)
    obs.signal_handler_connect(signal_handler,"stop",load_stop_url_cb)
    obs.obs_output_release(output)
    
def remove_output_callbacks(output_name):
    output = obs.obs_get_output_by_name(output_name)
    signal_handler = obs.obs_output_get_signal_handler(output)
    obs.signal_handler_disconnect(signal_handler,"start",load_start_url_cb)
    obs.signal_handler_disconnect(signal_handler,"stop",load_stop_url_cb)
    obs.obs_output_release(output)

def script_load(settings):
    register_output_callbacks("simple_stream")
    register_output_callbacks("adv_stream")
    register_output_callbacks("ffmpeg_output")
    register_output_callbacks("simple_file_output")
    register_output_callbacks("adv_file_output")
    register_output_callbacks("adv_ffmpeg_output")

def script_unload():
    remove_output_callbacks("simple_stream")
    remove_output_callbacks("adv_stream")
    remove_output_callbacks("ffmpeg_output")
    remove_output_callbacks("simple_file_output")
    remove_output_callbacks("adv_file_output")
    remove_output_callbacks("adv_ffmpeg_output")


def script_defaults(settings):
    pass

def script_properties():
    props = obs.obs_properties_create()

    obs.obs_properties_add_text(props, "starturl", "Start URL", obs.OBS_TEXT_DEFAULT)
    obs.obs_properties_add_text(props, "stopurl", "Stop URL", obs.OBS_TEXT_DEFAULT)

    obs.obs_properties_add_button(props, "startbutton", "Test Start URL", test_start_url)
    obs.obs_properties_add_button(props, "stopbutton", "Test Stop URL", test_stop_url)
    return props
