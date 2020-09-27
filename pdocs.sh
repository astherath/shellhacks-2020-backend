git checkout gh-pages
redoc-cli bundle http://localhost:5000/openapi.json
mv redoc-static.html index.html
git add .
git commit -am "updated docs"
git push
git checkout master
