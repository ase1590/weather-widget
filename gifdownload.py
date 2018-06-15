import os
import time
import requests

class grabber:
    """
    provides tools for grabbing images
    usage: grabber('url')
    """
    def __init__(self, url_name):
        self.url_name = url_name

    def downloadCheck(self,out_name):
        """
        downloads a file, then checks to see if it exists.
        If it does, waits 15 minutes before grabbing a new one.
        usage: downloadCheck("filename.xxx")
        """

        def downloader():
            try:
                print("downloading, please wait")
                r = requests.get(self.url_name)
                if r.ok:
                    open(out_name, 'wb').write(r.content)
                else:
                    r.raise_for_status()

            except requests.ConnectionError:
                print("could not fetch gif, check connection")
                # print("error",sys.exc_info()[0])

            except requests.HTTPError:
                print("Error getting url data")
                print(r)
            except:
                raise

        if os.path.isfile(out_name) == True:
            print("checking update")
            u = os.path.getmtime(out_name)
            agediff = 900
            if time.time() > u + agediff:
                downloader()
                print("updated gif")
            else:
                print("nothing to update")
        else:
            print("downloading initial file, please wait")
            r = requests.get(self.url_name)
            if r.ok:
                open(out_name, 'wb').write(r.content)
            else:
                r.raise_for_status()

    def SimpleDownload(self,out_name):
        "SimpleDownload('output.xxxx'): downloads a file"
        print("downloading...")
        r = requests.get(self.url_name)
        if r.ok:
            open(out_name, 'wb').write(r.content)
            print("download complete")
        else:
            r.raise_for_status()


#r = GifGrabber('http://radar.weather.gov/ridge/Conus/Loop/NatLoop.gif')
