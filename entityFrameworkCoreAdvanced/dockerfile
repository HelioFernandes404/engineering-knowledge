#See https://aka.ms/customizecontainer to learn how to customize your debug container and how Visual Studio uses this Dockerfile to build your images for faster debugging.

# cria 1. imagem e dar um aplido chamado base 
FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS base
WORKDIR /app
EXPOSE 80 
EXPOSE 443

# instalar o sdk e build nossa aplicação gerando os binarios
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["DominandoEFCore.csproj", "DominandoEFCore/"]
RUN dotnet restore "DominandoEFCore/DominandoEFCore.csproj"
WORKDIR "/DominandoEFCore"
COPY . .

RUN dotnet build "./DominandoEFCore.csproj" -c Release -o /app/build

RUN dotnet dev-certs https -ep /root/.aspnet/https/aspnetapp.pfx -p 1234
RUN dotnet dev-certs https --trust

# passa o build para uma pagina publish
FROM build AS publish
COPY --from=build /root/.aspnet/https/aspnetapp.pfx /root/.aspnet/https/
RUN dotnet publish "./DominandoEFCore.csproj" -c Release -o /app/publish

# Build e da run nossa imagem final 
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
COPY --from=publish /root/.aspnet/https/aspnetapp.pfx /root/.aspnet/https/
ENV ASPNETCORE_ENVIRONMENT=Development
ENV ASPNETCORE_URLS="https://+:80;https://+:443;"
ENV ASPNETCORE_kestrel__Certificates__Default__Password="1234"
ENV ASPNETCORE_kestrel__Certificates__Default__Path="/root/.aspnet/https/aspnetapp.pfx"
ENTRYPOINT ["dotnet", "DominandoEFCore.dll"]