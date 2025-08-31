echo "Enter your choice (start/stop/status)"
read choice
case $choice in
start)
    echo "service stated...."
    ;;
stop)
    echo "service stopped....."
    ;;
status)
    echo "service is running"
    ;;
*)
    echo "Entered incorrect choice"
    ;;
esac