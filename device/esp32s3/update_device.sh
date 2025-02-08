echo "Load environment for esp32s3"

# Load the esp32s3 supported devices
pushd sdk/esp-idf > /dev/null

./install.sh
source export.sh

popd > /dev/null