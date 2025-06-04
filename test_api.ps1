$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    url = "https://en.wikipedia.org/wiki/Artificial_intelligence"
    content_type = "url"
    use_ai = $true
    settings = @{
        duration = 60
        voice_style = "professional"
        language = "en"
    }
} | ConvertTo-Json

Write-Host "Testing /api/process endpoint..."
try {
    $response = Invoke-RestMethod -Uri "https://tiktok-video-generator-production-ea7b.up.railway.app/api/process" -Method Post -Headers $headers -Body $body
    Write-Host "✅ SUCCESS:"
    $response | ConvertTo-Json -Depth 3
} catch {
    Write-Host "❌ ERROR:"
    Write-Host $_.Exception.Message
    if ($_.Exception.Response) {
        Write-Host "Status Code:" $_.Exception.Response.StatusCode
        Write-Host "Status Description:" $_.Exception.Response.StatusDescription
    }
} 