import multiprocessing

user      = 'www-data'
group     = 'www-data'
bind      = '0.0.0.0:80'
workers   = 1 # multiprocessing.cpu_count() * 2 + 1
threads   = workers
accesslog = '-'
errorlog = '-'
