
#!/bin/bash

# 1. requirements.txt에 있는 패키지가 설치되지 않은 것이 있다면 설치
echo "Checking and installing required packages..."
pip install -r requirements.txt

# 2. 현재 실행 중인 process 중 check.py가 있다면 해당 process를 종료
echo "Checking for existing check.py process..."
PIDS=$(pgrep -f check.py)
if [ -n "$PIDS" ]; then
    echo "Existing process found. Terminating..."
    kill $PIDS
fi

# 3. 자신의 tmux 세션 이름을 선언하고, 해당 세션과 같은 이름의 세션이 없다면 생성
SESSION_NAME="my_tmux_session"
tmux has-session -t $SESSION_NAME 2>/dev/null

if [ $? != 0 ]; then
    echo "Starting new tmux session..."
    tmux new-session -d -s $SESSION_NAME
fi

# 4. 해당 tmux 세션에서 check.py를 실행
echo "Starting Python script in tmux session..."
tmux send-keys -t $SESSION_NAME "python3 /path/to/check.py" C-m

echo "Script execution initiated in tmux session."
