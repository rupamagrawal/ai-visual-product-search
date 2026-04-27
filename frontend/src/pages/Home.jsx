import { useState } from "react";
import Upload from "../components/Upload";
import ResultCard from "../components/ResultCard";
import { searchByImage } from "../api";

function Home() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [results, setResults] = useState([]);

  const handleUpload = async (file) => {
    setLoading(true);
    setError("");

    try {
      const data = await searchByImage(file);
      setAnalysis({
        object: data.object,
        color: data.color,
        query: data.query,
      });
      setResults(data.results || []);
    } catch (err) {
      setError(err.message || "Something went wrong");
      setResults([]);
      setAnalysis(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto max-w-6xl px-4 py-10">
      <header className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-slate-900">
          AI Visual Product Search
        </h1>
        <p className="mt-2 max-w-3xl text-slate-600">
          Upload one image. The backend predicts the object and dominant color, then
          searches shopping websites using that combined query.
        </p>
      </header>

      <div className="grid gap-6 md:grid-cols-[340px_1fr]">
        <Upload onUpload={handleUpload} loading={loading} />

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          {error ? <p className="mb-4 text-sm text-red-600">{error}</p> : null}

          {analysis ? (
            <div className="mb-6 grid gap-2 rounded-lg bg-slate-50 p-4 text-sm">
              <p>
                <span className="font-semibold">Detected Object:</span> {analysis.object}
              </p>
              <p>
                <span className="font-semibold">Dominant Color:</span> {analysis.color}
              </p>
              <p>
                <span className="font-semibold">Search Query:</span> {analysis.query}
              </p>
            </div>
          ) : (
            <p className="mb-6 text-sm text-slate-600">
              No image analyzed yet. Upload an image to start.
            </p>
          )}

          <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
            {results.map((item, index) => (
              <ResultCard key={`${item.link || "item"}-${index}`} item={item} />
            ))}
          </div>
        </section>
      </div>
    </main>
  );
}

export default Home;
