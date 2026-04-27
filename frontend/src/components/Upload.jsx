import { useState } from "react";

function Upload({ onUpload, loading }) {
  const [file, setFile] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (!file) {
      return;
    }
    onUpload(file);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"
    >
      <label className="mb-3 block text-sm font-semibold text-slate-700">
        Upload product image
      </label>
      <input
        type="file"
        accept="image/*"
        onChange={(event) => setFile(event.target.files?.[0] || null)}
        className="mb-4 block w-full rounded-lg border border-slate-200 p-2 text-sm"
      />
      <button
        type="submit"
        disabled={loading || !file}
        className="w-full rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-slate-400"
      >
        {loading ? "Analyzing image..." : "Find Similar Products"}
      </button>
    </form>
  );
}

export default Upload;
