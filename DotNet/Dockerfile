
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

WORKDIR /src


COPY dotnet-app.csproj ./
RUN dotnet restore

COPY Program.cs ./
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/runtime:8.0

WORKDIR /app
COPY --from=build /app/publish .

ENV TELEGRAM_BOT_TOKEN=""
ENV TELEGRAM_CHAT_ID=""

ENTRYPOINT ["dotnet", "dotnet-app.dll"]
