"""Constants and mappings for LinkedIn URL parameters."""

# LinkedIn parameter mappings
WORKPLACE_TYPE_MAP = {"onsite": "1", "hybrid": "3", "remote": "2"}

DATE_POSTED_MAP = {
    "hour": "r3600",
    "day": "r86400",
    "week": "r604800",
    "month": "r2592000",
}

# Recruitment search terms (PT-BR) - optimized based on testing
RECRUITMENT_TERMS_PT = ["vaga", "oportunidade", "contratando"]

REMOTE_WORK_TERMS_PT = ["remoto", "home office", "trabalho remoto"]

# Seniority options
SENIORITY_OPTIONS = ["Estágio", "Junior", "Pleno", "Senior"]

# Workplace type options with labels
WORKPLACE_TYPE_OPTIONS = {
    "onsite": "Presencial",
    "hybrid": "Híbrido",
    "remote": "Remoto",
}

# Date posted options with labels
DATE_POSTED_OPTIONS = {
    "any": "Qualquer período",
    "hour": "Última hora",
    "day": "Último dia",
    "week": "Última semana",
    "month": "Último mês",
}

# Experience level mappings (f_E parameter)
EXPERIENCE_LEVEL_MAP = {
    "internship": "1",
    "entry": "2",
    "associate": "3",
    "mid_senior": "4",
    "director": "5",
    "executive": "6",
}

EXPERIENCE_LEVEL_OPTIONS = {
    "internship": "Estágio",
    "entry": "Júnior (Entry Level)",
    "associate": "Pleno (Associate)",
    "mid_senior": "Sênior (Mid-Senior)",
    "director": "Diretor",
    "executive": "Executivo (C-Level)",
}

# Job type mappings (f_JT parameter)
JOB_TYPE_MAP = {
    "full_time": "F",
    "part_time": "P",
    "contract": "C",
    "temporary": "T",
    "internship": "I",
    "volunteer": "V",
    "other": "O",
}

JOB_TYPE_OPTIONS = {
    "full_time": "Tempo Integral (CLT)",
    "part_time": "Meio Período",
    "contract": "Contrato/PJ",
    "temporary": "Temporário",
    "internship": "Estágio",
    "volunteer": "Voluntário",
    "other": "Outros",
}

# Technology suggestions for autocomplete
TECH_SUGGESTIONS = [
    "React",
    "Angular",
    "Vue",
    "QA",
    "Frontend",
    "Node.js",
    "TypeScript",
    "Python",
    "Java",
]
