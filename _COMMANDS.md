  due                       # Standard: Datei-Gruppierung, nur @due-Tasks, ohne [x]/[c]
  due --sort-by-date        # Flache Liste, nach Datum sortiert (ältestes zuerst)
  due --include-undated     # Auch Tasks ohne @due
  due --include-closed      # Auch [x] und [c]
  due --when -1             # Nur überfällige Tasks
  due --when 0              # Nur heutige Tasks
  due --when 1              # Nur zukünftige Tasks
  due list --sort-by-date -u  # Expliziter list-Subcommand mit Flags
