# Search API for PPT-intro-pages
These are the files for the PPT introductory pages. These are written in Flask, HTML and JS.

### To start application with gunicorn

```
gunicorn Main:app --workers 4
```

### To run application as daemon for systems with upstart

Copy the upstart script (search.conf) to /etc/init and then edit it accordingly as commented out.

```
sudo cp search.conf /etc/init
```

After setup you can run the below commands:

```
service search start
service search stop
```

#### To run at boot-time
```
update-rc.d search defaults
```
