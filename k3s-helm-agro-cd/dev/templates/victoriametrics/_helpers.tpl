{{- define "victoriametrics.name" -}}
victoriametrics
{{- end -}}

{{- define "victoriametrics.fullname" -}}
{{ include "victoriametrics.name" . }}-{{ .Release.Name }}
{{- end -}}

{{- define "victoriametrics.chart" -}}
{{ .Chart.Name }}-{{ .Chart.Version }}
{{- end -}}
