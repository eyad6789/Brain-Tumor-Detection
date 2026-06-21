"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";

/** Accent color palettes. "cyan" is the default (base CSS, no data-palette). */
export const PALETTES = [
  { id: "cyan", label: "Cyan", swatch: ["#2cd4ee", "#8b7bff"] },
  { id: "rose", label: "Rose", swatch: ["#ff5d8f", "#c08bff"] },
  { id: "violet", label: "Violet", swatch: ["#a78bff", "#3dd6e6"] },
  { id: "emerald", label: "Emerald", swatch: ["#34d39a", "#2cd4ee"] },
] as const;

export type PaletteId = (typeof PALETTES)[number]["id"];

export const PALETTE_STORAGE_KEY = "neuroscan-palette";

function apply(id: PaletteId) {
  const el = document.documentElement;
  if (id === "cyan") el.removeAttribute("data-palette");
  else el.setAttribute("data-palette", id);
}

type PaletteContextValue = {
  palette: PaletteId;
  setPalette: (id: PaletteId) => void;
};

const PaletteContext = createContext<PaletteContextValue | null>(null);

export function PaletteProvider({ children }: { children: React.ReactNode }) {
  const [palette, setPaletteState] = useState<PaletteId>("cyan");

  // Sync React state with what the no-flash inline script already applied.
  useEffect(() => {
    try {
      const saved = localStorage.getItem(PALETTE_STORAGE_KEY) as PaletteId | null;
      if (saved && PALETTES.some((p) => p.id === saved)) {
        setPaletteState(saved);
        apply(saved);
      }
    } catch {
      /* localStorage may be unavailable; fall back to default */
    }
  }, []);

  const setPalette = useCallback((id: PaletteId) => {
    setPaletteState(id);
    apply(id);
    try {
      localStorage.setItem(PALETTE_STORAGE_KEY, id);
    } catch {
      /* ignore */
    }
  }, []);

  return (
    <PaletteContext.Provider value={{ palette, setPalette }}>
      {children}
    </PaletteContext.Provider>
  );
}

export function usePalette() {
  const ctx = useContext(PaletteContext);
  if (!ctx) throw new Error("usePalette must be used within a PaletteProvider");
  return ctx;
}

/** Inline script body that applies the saved palette before first paint. */
export const PALETTE_NO_FLASH_SCRIPT = `(function(){try{var p=localStorage.getItem('${PALETTE_STORAGE_KEY}');if(p&&p!=='cyan'){document.documentElement.setAttribute('data-palette',p);}}catch(e){}})();`;
