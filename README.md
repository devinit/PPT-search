# PPT-intro-pages
These are the files for the PPT introductory pages. These are written in Flask, HTML and JS

### To start application with gunicorn

gunicorn Main:app --workers 16

### To run application as daemon

```
service search start
service search stop
```

#### To run at boot-time

update-rc.d search defaults
