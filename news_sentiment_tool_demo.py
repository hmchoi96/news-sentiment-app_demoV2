<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>WISERBOND – News Sentiment Dashboard</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 0;
      background: #f4f4f4;
    }
    .container {
      max-width: 1200px;
      margin: auto;
      padding: 20px;
    }
    header {
      background: #1a1a1a;
      color: white;
      padding: 20px;
      text-align: center;
    }
    .section {
      background: white;
      padding: 20px;
      margin-top: 20px;
      border-radius: 8px;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .flex {
      display: flex;
      gap: 20px;
      flex-wrap: wrap;
    }
    .pie-chart {
      width: 200px;
      height: 200px;
      background: conic-gradient(red 70%, orange 20%, green 10%);
      border-radius: 50%;
      margin: auto;
    }
    h2 {
      color: #333;
    }
    .source-group {
      margin-top: 10px;
    }
    .tag {
      display: inline-block;
      background: #eee;
      padding: 5px 10px;
      margin: 5px;
      border-radius: 4px;
    }
  </style>
</head>
<body>

<header>
  <h1>WISERBOND – News Sentiment Dashboard</h1>
</header>

<div class="container">

  <div class="section">
    <h2>Search & Filter</h2>
    <input type="text" placeholder="Search topic..." style="width: 60%; padding: 10px;">
    <input type="date" style="padding: 10px;">
  </div>

  <div class="section flex">
    <div style="flex: 1;">
      <h2>Sentiment Breakdown</h2>
      <div class="pie-chart"></div>
      <ul>
        <li><span style="color: red;">■</span> Negative: 70%</li>
        <li><span style="color: orange;">■</span> Neutral: 20%</li>
        <li><span style="color: green;">■</span> Positive: 10%</li>
      </ul>
    </div>
    <div style="flex: 2;">
      <h2>Topic Overview: USA’s Tariff</h2>
      <p>This analysis summarizes coverage from N media outlets on the selected topic.</p>
      <img src="thumbnail.jpg" alt="Representative" style="width: 100%; max-width: 300px;">
    </div>
  </div>

  <div class="section">
    <h2>AI Summary</h2>
    <strong>Positive View:</strong>
    <p>[Add positive summaries here]</p>
    <strong>Negative View:</strong>
    <p>President Trump unveils double-digit tariffs... PSA halts non-US submissions in response to tariffs.</p>
  </div>

  <div class="section">
    <h2>Wiserbond’s View</h2>
    <p>[Add Wiserbond’s interpretation here]</p>

    <h2>Experts’ View</h2>
    <p>[Add expert quotes or analysis here]</p>
  </div>

  <div class="section">
    <h2>Media Source Breakdown</h2>
    <div class="source-group">
      <strong>Neutral:</strong>
      <span class="tag">CNN</span> <span class="tag">Reuters</span>
    </div>
    <div class="source-group">
      <strong>Negative:</strong>
      <span class="tag">Fox News</span> <span class="tag">NYT</span>
    </div>
    <div class="source-group">
      <strong>Positive:</strong>
      <span class="tag">WSJ</span> <span class="tag">Bloomberg</span>
    </div>
  </div>

</div>

</body>
</html>
