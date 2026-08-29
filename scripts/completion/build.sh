# source scripts/completion/build.sh

_build_sh_completion() {
    local cur prev targets

    targets="
        all
        config
        metadata
        og-generate
        og-build
        og-refresh
        metadata-check
        generated
        imports
        links
        og-check
        prepare-dist
        prepare-diagnostics
        html
        sitemap
        robots
        pdf
        categories
        book
        pages-pdf
        allpdf
        report
    "

    cur="${COMP_WORDS[COMP_CWORD]}"

    COMPREPLY=(
        $(compgen -W "$targets" -- "$cur")
    )
}

complete -F _build_sh_completion ./build.sh