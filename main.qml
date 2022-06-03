import QtQuick 2.15
import QtQuick.Controls 2.15
ApplicationWindow {
    visible: true
    width: 448
    height: 470
    title: "Encryption Tool"

    Rectangle {
        width: 448
        height: 470
        visible: true
        color: "#000000"

        ToolButton {
            id: select
            x: 115
            y: 65
            width: 220
            height: 48
            text: qsTr("Select Folder")
            highlighted: true
            font.pointSize: 13
            flat: true
        }
        Label {
            id: selected_folder
            x: 115
            y: 119
            width: 219
            height: 34
            text: qsTr("No Folder Selected")
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pointSize: 13
            scale: 1
        }

        TextField {
            id: passcode
            x: 115
            y: 271
            width: 219
            height: 32
            text: "Passcode"
            placeholderText: qsTr("Text Field")
        }

        Label {
            id: passcode_label
            x: 115
            y: 218
            width: 219
            height: 34
            text: qsTr("Enter Passcode")
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            font.pointSize: 13
            scale: 1
        }

        ToolButton {
            id: decrypt
            x: 35
            y: 376
            width: 180
            height: 55
            text: qsTr("Decrypt")
            highlighted: true
            flat: true
            font.pointSize: 13
        }

        ToolButton {
            id: encrypt
            x: 233
            y: 376
            width: 180
            height: 55
            text: qsTr("Encrypt")
            highlighted: true
            flat: true
            font.pointSize: 13
        }
    }


}
