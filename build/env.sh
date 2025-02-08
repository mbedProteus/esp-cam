#!/bin/bash

LUNCH_MENU=""

# Function to set the target product and device folder
# Usage: lunch <app_name>_<device>_<variant>
# Example: lunch cam_esp32_debug
add_lunch_combo() {
    local target=$1
    if [ -z "$target" ]; then
        echo "Usage: add_lunch_combo <app_name>_<device>_<variant>"
        return 1
    fi

    IFS='_' read -r app_name device variant <<< "$target"

    if [[ "$device" != esp32* ]]; then
        echo "Error: Device must be from the esp32 family."
        return 1
    fi

    if [[ "$variant" != "debug" && "$variant" != "release" ]]; then
        echo "Error: Variant must be either 'debug' or 'release'."
        return 1
    fi

    LUNCH_MENU="$LUNCH_MENU $target"
}

query_targets() {
    LUNCH_MENU=""  # Clean LUNCH_MENU before querying targets
    local app_folder="app"
    if [ -d "$app_folder" ]; then
        for app in "$app_folder"/*; do
            if [ -d "$app" ]; then
                local supported_devices_file="$app/supported_devices.sh"
                if [ -f "$supported_devices_file" ]; then
                    source "$supported_devices_file" || {
                        echo "Error sourcing supported devices file: $supported_devices_file"
                        return 1
                    }
                else
                    echo "Supported devices file not found: $supported_devices_file"
                fi
            else
                echo "App subfolder not found: $app"
            fi
        done
    else
        return 1
    fi
}

lunch() {
    if [ -n "$1" ]; then
        local target=$1
        for combo in $LUNCH_MENU; do
            if [[ "$combo" == "$target" ]]; then
                echo "You selected: $target"
                return 0
            fi
        done
        echo "Invalid target: $target"
        return 1
    fi

    if [ -z "$LUNCH_MENU" ]; then
        echo "No lunch combos available."
        return 1
    fi

    echo "Available lunch combos:"
    local index=1
    declare -A combo_map
    for combo in $LUNCH_MENU; do
        echo "  $index. $combo"
        combo_map[$index]=$combo
        ((index++))
    done

    read -p "Select a combo by number: " selection
    if [[ ! $selection =~ ^[0-9]+$ ]] || [ -z "${combo_map[$selection]}" ]; then
        echo "Invalid selection."
        return 1
    fi

    selected_combo=${combo_map[$selection]}
    echo "You selected: $selected_combo"

    IFS='_' read -r app_name device variant <<< "$selected_combo"
    
    if [[ "$device" == esp32* ]]; then
        echo "Set target for idf is $device"
        export IDF_TARGET=$device
    fi
    
    source device/$device/update_device.sh || {
        echo "Error sourcing device update script: device/$device/update_device.sh"
        return 1
    }
}

# Function to provide auto-completion for the lunch command
_lunch_completion() {
    local cur_word="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=($(compgen -W "$LUNCH_MENU" -- "$cur_word"))
}

# Register the _lunch_completion function for the lunch command
complete -F _lunch_completion lunch

query_targets
