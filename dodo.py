import subprocess
import os
from datetime import datetime
from colorama import *
init() #colorama initialization

### task setup env
DOIT_CONFIG = {'verbosity': 2, 'default_tasks': ['build']}

###############################################################################################
############## CONFIGURATION ##################################################################
###############################################################################################
projects = [
            'unittests\\UnitTests.dproj',
            'samples\\01_global_logger\\global_logger.dproj',
						'samples\\02_file_appender\\file_appender.dproj',
						'samples\\03_console_appender\\console_appender.dproj',
						'samples\\04_outputdebugstring_appender\\outputdebugstring_appender.dproj',
						'samples\\05_vcl_appenders\\memo_appender.dproj',
						'samples\\10_multiple_appenders\\multiple_appenders.dproj',
						'samples\\20_multiple_loggers\\multiple_loggers.dproj',
						'samples\\50_custom_appender\\custom_appender.dproj'											
            ]
release_path = "BUILD"
###############################################################################################
############## END CONFIGURATION ##############################################################
###############################################################################################

GlobalBuildVersion = 'DEV' #if we are building an actual release, this will be replaced

def header(headers):    
    elements = None
    if type(headers).__name__ == 'str':
        elements = [headers]
    else:
        elements = headers

    print(Style.BRIGHT + Back.WHITE + Fore.RED + "*" * 70 + Style.RESET_ALL)
    for txt in elements:
        s = '{:^70}'.format(txt)
        print(Style.BRIGHT + Back.WHITE + Fore.RED + s + Style.RESET_ALL)       
    print(Style.BRIGHT + Back.WHITE + Fore.RED + "*" * 70 + Style.RESET_ALL)        
    

def buildProject(project, config = 'DEBUG'):
    header(["Building", project,"(config " + config + ")"])
    p = project.replace('.dproj', '.cfg')
    if os.path.isfile(p):
      if os.path.isfile(p + '.unused'):
        os.remove(p + '.unused')
      os.rename(p, p + '.unused')
    return subprocess.call("rsvars.bat & msbuild /t:Build /p:Config=" + config + " /p:Platform=Win32 \"" + project + "\"", shell=True) == 0

def buildProjects():
    for project in projects:
      res = buildProject(project)
      if not res:
        return False
    return True


def create_build_tag(version):
    global GlobalBuildVersion
    GlobalBuildVersion = version
    header("BUILD VERSION: " + GlobalBuildVersion)
    f = open("VERSION.TXT","w")
    f.write("VERSION " + GlobalBuildVersion + "\n")
    f.write("BUILD DATETIME " + datetime.now().isoformat() + "\n")
    f.close()

#############################################################################################################################

def task_build():
    '''Use: doit build -v <VERSION> -> Builds all the projects, and "HOAsys Tools" setup. Then creates SFX archive.'''    
    return {
        'actions': [create_build_tag,
            "echo %%date%% %%time:~0,8%% > LOGGERPRO-BUILD-TIMESTAMP.TXT",            
            buildProjects,
						"unittests\\Win32\\Debug\\UnitTests.exe -exit:Continue"],
	'params':[{'name':'version',
	           'short':'v',
	           'long':'version',
             'type':str,
             'default':'DEVELOPMENT'}
             ],						
        'verbosity': 2
        }
