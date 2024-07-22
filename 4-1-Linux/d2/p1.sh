pip install -r requirements.txt
pkill -f check.py
TMUX_SESSION_NAME="my_tmux_session"
if ! tmux has-session -t $TMUX_SESSION_NAME 2>/dev/null; then
    
    tmux new-session -d -s $TMUX_SESSION_NAME
tmux send-keys -t $TMUX_SESSION_NAME "python check.py" C-m
fi
