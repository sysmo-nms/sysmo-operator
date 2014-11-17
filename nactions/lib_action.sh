lib_action_get() {
    case $1 in
        Ip)
            echo -n "192.168.0.5";;
        Probe)
            case $2 in
                *)
                    echo -n "undefined";;
            esac;;
        *)
            echo -n "undefined";;
    esac
}

lib_action_pretty_print() {
    echo "all env"
}

lib_action_init() {
    NOCTOPUS="read values from ENV and store it for lib_action_get"
}

lib_action_init
