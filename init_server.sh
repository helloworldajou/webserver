sudo cp nginx.conf /etc/nginx/sites-enabled/
service postgresql start
service nginx restart
psql -U postgres < "./init_db.sql"
python manage.py makemigrations
python manage.py migrate
mkdir ./data/faces/aligned
mkdir ./data/faces/feature
for N in {1..8}; do ./util/align-dlib.py ./data/faces/raw align outerEyesAndNose ./data/faces/aligned --size 96 & done
./batch-represent/main.lua -outDir ./data/faces/feature -data ./data/faces/aligned
./demos/classifier.py train ./data/faces/feature