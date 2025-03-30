import { NextResponse } from 'next/server';
import { spawn } from 'child_process';
import { promises as fs } from 'fs';
import path from 'path';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const symbol = searchParams.get('symbol');

  if (!symbol) {
    return NextResponse.json({ error: 'Symbol is required' }, { status: 400 });
  }

  try {
    // Run the Python analysis script
    const analysisProcess = spawn('python', [
      '-m',
      'src.main',
      symbol,
      '-o',
      'analysis_results'
    ]);

    // Wait for the analysis to complete
    await new Promise((resolve, reject) => {
      analysisProcess.on('close', (code) => {
        if (code === 0) {
          resolve(null);
        } else {
          reject(new Error(`Analysis process exited with code ${code}`));
        }
      });
    });

    // Read the analysis results
    const resultsPath = path.join(process.cwd(), 'analysis_results', `${symbol}_analysis.json`);
    const analysisData = await fs.readFile(resultsPath, 'utf-8');
    const analysis = JSON.parse(analysisData);

    return NextResponse.json(analysis);
  } catch (error) {
    console.error('Error analyzing stock:', error);
    return NextResponse.json(
      { error: 'Failed to analyze stock' },
      { status: 500 }
    );
  }
} 