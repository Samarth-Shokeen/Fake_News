import React, { useState } from 'react';
import { CheckCircle, XCircle, Loader2, Zap } from 'lucide-react';

interface VerificationResult {
  isValid: boolean;
}

function App() {
  const [headline, setHeadline] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<VerificationResult | null>(null);
  const [error, setError] = useState('');

  const handleVerify = async () => {
    if (!headline.trim()) {
      setError('Please enter a headline to verify');
      return;
    }

    setIsLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/check', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_string: headline.trim() }),
      });

      if (!response.ok) {
        throw new Error('Failed to verify headline');
      }

      const data = await response.json();
      const isValid = data.result === 'Real';

      setResult({ isValid });
    } catch (err) {
      setError('Failed to verify headline. Please try again.');
    }

    setIsLoading(false);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleVerify();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-600 rounded-full mb-4">
            <Zap className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Headline Verifier
          </h1>
          <p className="text-gray-600">
            Enter your headline to verify its effectiveness
          </p>
        </div>

        <div className="bg-white rounded-2xl shadow-lg border border-gray-100 p-8">
          <div className="space-y-6">
            <div>
              <textarea
                value={headline}
                onChange={(e) => {
                  setHeadline(e.target.value);
                  setError('');
                  setResult(null);
                }}
                onKeyPress={handleKeyPress}
                placeholder="Enter your headline here..."
                className="w-full px-4 py-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 resize-none text-lg"
                rows={3}
                maxLength={200}
              />
              <div className="flex justify-between items-center mt-2">
                <div className="text-sm text-gray-400">{headline.length}/200</div>
                {error && <p className="text-sm text-red-600">{error}</p>}
              </div>
            </div>

            <button
              onClick={handleVerify}
              disabled={isLoading || !headline.trim()}
              className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-semibold py-4 px-6 rounded-xl transition-all duration-200 flex items-center justify-center space-x-2 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Verifying...</span>
                </>
              ) : (
                <span>Verify Headline</span>
              )}
            </button>

            {result && (
              <div className="pt-4 border-t border-gray-100">
                <div
                  className={`flex items-center justify-center space-x-3 p-6 rounded-xl ${
                    result.isValid
                      ? 'bg-green-50 border border-green-200'
                      : 'bg-red-50 border border-red-200'
                  }`}
                >
                  {result.isValid ? (
                    <>
                      <CheckCircle className="w-8 h-8 text-green-600" />
                      <div className="text-center">
                        <div className="text-xl font-bold text-green-800">Valid</div>
                        <div className="text-sm text-green-600">
                          This headline looks good!
                        </div>
                      </div>
                    </>
                  ) : (
                    <>
                      <XCircle className="w-8 h-8 text-red-600" />
                      <div className="text-center">
                        <div className="text-xl font-bold text-red-800">Invalid</div>
                        <div className="text-sm text-red-600">
                          This headline needs improvement
                        </div>
                      </div>
                    </>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
