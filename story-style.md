# Hanna Story – Visual Style Guide

## Format
- Instagram Story: 1080 × 1920px (9:16)
- Hintergrundbild: Creator-Foto (wird immer frisch vorgegeben, deckt gesamtes Format ab)
- `background-size: cover`, `background-position: center top`

## Text-Boxen
- Hintergrundfarbe: `#111111` (nahezu schwarz, kein Transparenz-Effekt)
- Textfarbe: `#ffffff`
- Border-Radius: `0` (scharfe Ecken)
- Padding: `10px 14px`
- Abstand zwischen Boxen: `8px`
- Breite: `calc(100% - 32px)`, also volle Breite mit 16px Rand links und rechts
- Display: `block`

## Typografie
- Font: `'Inter', Arial, sans-serif`
- Font-Weight: `700` (Bold)
- Font-Size: `18px`
- Line-Height: `1.4`
- Text-Align: `left`

## Positionierung der Text-Boxen
- Positioniert im unteren Bereich des Bildes
- Container: `position: absolute`, `bottom: 40px`, `left: 16px`, `right: 16px`
- Jeder Sinnabschnitt bekommt eine eigene Box

## Struktur (HTML-Template)
```html
<div class="story">
  <div class="bg" style="background-image: url('BILD_HIER')"></div>
  <div class="text-area">
    <div class="box">Text 1</div>
    <div class="box">Text 2</div>
    <!-- ... -->
  </div>
</div>
```

## CSS-Kern
```css
.story { position: relative; width: 1080px; height: 1920px; overflow: hidden; }
.bg { position: absolute; inset: 0; background-size: cover; background-position: center top; }
.text-area { position: absolute; bottom: 40px; left: 16px; right: 16px; display: flex; flex-direction: column; gap: 8px; }
.box { background: #111111; color: #ffffff; font-family: 'Inter', Arial, sans-serif; font-size: 18px; font-weight: 700; line-height: 1.4; padding: 10px 14px; }
```
