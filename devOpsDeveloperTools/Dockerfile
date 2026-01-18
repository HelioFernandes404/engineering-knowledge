# Stage 1: Build
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS builder
WORKDIR /build
COPY . .
RUN dotnet publish -c Release -o /app

# Stage 2: Final
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=builder /app .
ENTRYPOINT ["dotnet", "projeto-multi-stage-builds.dll"]