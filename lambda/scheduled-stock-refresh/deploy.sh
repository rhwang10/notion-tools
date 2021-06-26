pushd ~/.pyenv/versions/venv/lib/python3.8/site-packages
zip -r9 ${OLDPWD}/lambda.zip .
popd
zip -g lambda.zip lambda_function.py
aws lambda update-function-code --function-name scheduled-stock-refresh --zip-file fileb://lambda.zip
