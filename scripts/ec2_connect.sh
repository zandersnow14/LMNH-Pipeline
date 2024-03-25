source .env
chmod 400 $PEMKEY
ssh -i $PEMKEY $EC2_USER@$EC2_URL