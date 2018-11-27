import subprocess
import os
##hyperparam
required_time=2
wav_name=1
exe_name="\\wasapi_capture.exe"


current_dir,fn=os.path.split(__file__)
full_path=current_dir+exe_name
subprocess.call(
full_path+" "+str(wav_name)+" "+str(required_time))


