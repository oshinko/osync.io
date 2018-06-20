#!/bin/sh

hugo -t osync.io --cleanDestinationDir
cd public
cat <<EOF> CNAME
osync.io
EOF
python3 -m http.server

echo "Do you want to deploy? [Y/n]"
read ANSWER

case $ANSWER in
    "" | "Y" | "y" | "yes" | "Yes" | "YES" )
      echo "Start deployment."
      git init
      git remote add origin git@github.com:oshinko/osync.io-public.git
      git add .
      git reset *.DS_Store
      git commit -m 'Deployment commit'
      git push origin master -f
      echo "Deployment is complete."
      ;;
    * )
      echo "Deployment has been canceled."
      ;;
esac
