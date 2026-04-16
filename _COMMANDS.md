  due                    # Standard: Datei-Gruppierung, nur @due-Tasks, ohne [x]/[c]
  due --sort             # Flache Liste, nach Datum sortiert (ältestes zuerst)
  due --all-tasks        # Auch Tasks ohne @due
  due --all-statuses     # Auch [x] und [c]
  due --when -1          # Nur überfällige Tasks
  due --when 0           # Nur heutige Tasks
  due --when 1           # Nur zukünftige Tasks
  due list --sort -a     # Expliziter list-Subcommand mit Flags

