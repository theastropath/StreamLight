# StreamLight
Script for OBS Studio which accesses a configurable URL when you start streaming (or recording), and accesses another configurable URL when you stop streaming.  This allows you to trigger actions based on whether you are streaming or not.

Add the script to your OBS installation in the Scripts menu (Tools > Scripts).  
Ensure you have your Python path defined in the "Python Settings" tab.

Once the script has been added, enter the URL you want activated when the stream/recording is started in the "Start URL" box, and
the URL you want activated when stopping in the "Stop URL" box.  If you want the URLs to only be called for streaming or recording,
tick the appropriate "Enable for..." boxes.  URLs can be tested with the two "Test" buttons, to ensure they have been entered correctly.

Due to issues with the Python interface, the script has to check periodically whether OBS is streaming/recording or not.  "Check Interval"
defines how many seconds between these checks in seconds.  1 second doesn't seem to cause issues, but it can be set to check less
frequently if it causes problems on your system.
