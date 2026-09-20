
while true
do
	echo "Checking GitHub..."

	git fetch origin

	LOCAL=$(git rev-parse HEAD)
	REMOTE=$(git rev-parse origin/main)

	if [ "$LOCAL" != "$REMOTE" ]; then
		echo "New code detected!"

		git pull origin main

		echo "Running program..."
		python3 hello.py
	else
		echo "No update."

	fi

	sleep 10

done
