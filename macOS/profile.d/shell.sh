source_profile() {
    if [ "$SHELL" = "/bin/zsh" ] || [ "$SHELL" = "/usr/bin/zsh" ]; then
        for file in ~/profile.d/zsh/*.sh; do
            source "$file"
        done
    elif [ "$SHELL" = "/bin/bash" ] || [ "$SHELL" = "/usr/bin/bash" ]; then
        for file in ~/profile.d/bash/*.sh; do
            source "$file"
        done
    fi
}

