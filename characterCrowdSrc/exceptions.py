import sys, traceback
import pymel.core as pm

class CCCoreException(Exception):
    pass

class CCGuiException(Exception):
    pass

def wrapper(fn):
    """
    Wraps exception handler
    around common functions
    to write trace and popup gui dialogs
    """
    def innerWrapper(*args, **kwargs):
        try:
            result = fn(*args, **kwargs)
            return result
        except CCGuiException as e:
            pm.confirmDialog(
                    title="CharacterCrowd Error",
                    message=str(e),
                    button=["OK"]
            )
        except CCCoreException as e:
            print("CharacterCrowd:")
            print(str(e))
            pm.confirmDialog(
                    title="CharacterCrowd Error",
                    message=str(e),
                    button=["OK"],
            )
        except:
            print("CharacterCrowd Exception:")
            print('-'*60)
            traceback.print_exc(file=sys.stdout)
            print('-'*60)
    return innerWrapper
