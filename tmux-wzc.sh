
# create a new session: -s [session name] -n [window name] -d 分离
tmux new-session -s wzc-dev -n vim -d

# target [session]:[window].[pane]
tmux new-window -n panel -t wzc-dev
tmux split-window -h -t wzc-dev:2 # 2.2 redis
tmux split-window -v -t wzc-dev:2 # 2.3 phamtomjs
tmux split-window -v -t wzc-dev:2 # 2.4 celery
tmux new-window -n server -t wzc-dev
tmux split-window -v -t wzc-dev: # 2.4 celery

# window for vim
tmux send-keys -t wzc-dev:1.1 C-m # the first line usually is 'no session hint'
tmux send-keys -t wzc-dev:1.1 'cd ~/Documents/wzc/' C-m
tmux send-keys -t wzc-dev:1.1 'workon wzc' C-m
# tmux send-keys -t wzc-dev:1.1 'vim' C-m

# wondow for panel
tmux send-keys -t wzc-dev:2.1 'cd ~/Documents/wzc' C-m
tmux send-keys -t wzc-dev:2.1 'workon wzc' C-m


tmux send-keys -t wzc-dev:2.4 'cd ~/Documents/wzc/' C-m
tmux send-keys -t wzc-dev:2.4 'workon wzc' C-m
tmux send-keys -t wzc-dev:2.4 'redis-server' C-m


tmux send-keys -t wzc-dev:2.3 'cd ~/Documents/wzc/wzc/schedule/' C-m
tmux send-keys -t wzc-dev:2.3 'workon wzc' C-m
tmux send-keys -t wzc-dev:2.3 'celery -A tasks worker -l info' C-m

tmux send-keys -t wzc-dev:2.2 'cd ~/Documents/wzc/wzc/phantomjs/' C-m
tmux send-keys -t wzc-dev:2.2 'workon wzc' C-m
tmux send-keys -t wzc-dev:2.2 'phantomjs fetcher.js 12306' C-m

tmux send-keys -t wzc-dev:3 'workon wzc' C-m
tmux send-keys -t wzc-dev:3 'python ~/Documents/wzc/wzc/server/__init__.py' C-m

tmux select-layout -t wzc-dev:2.1 main-vertical 
# TODO: select first window of wzc-dev:2

# enter tmux, select vim window
tmux select-window -t wzc-dev:1
tmux attach -t wzc-dev



# refer
# https://pityonline.gitbooks.io/tmux-productive-mouse-free-development_zh/content/book-content/Chapter3.html
