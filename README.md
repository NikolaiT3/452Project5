# 452Project5

No one pushes to master - develop is the highest branch available to push


make sure repo is cloned

git checkout develop

git pull

git branch feature/yourFeatureName

git checkout feature/yourFeatureName

make your changes


once finished, push to your feature branch:

git add .

git commit -m “description of changes”

git push origin feature/yourFeatureName

git checkout develop

git pull

git merge feature/yourFeatureName

git add .

git commit -m “description of changes”

git push origin develop


to delete a branch

git branch -d feature/yourFeatureName
