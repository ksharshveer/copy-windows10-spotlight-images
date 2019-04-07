curl -L https://github.com/DevilLordHarsh/copy-windows10-spotlight-images/archive/master.zip > $TEMP/copy-windows10-spotlight-images-master.zip
unzip -o $TEMP/copy-windows10-spotlight-images-master.zip -d $HOME
rm $TEMP/copy-windows10-spotlight-images-master.zip

cd $HOME/copy-windows10-spotlight-images-master
pip install pipenv
pipenv install
echo 'alias get-spotlights="cd $HOME/copy-windows10-spotlight-images-master/; pipenv run python copy_spotlights.py"' >> $HOME/.bashrc
