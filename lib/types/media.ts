export interface PexelsPhoto {
  url: string
  photographer: string
  photographerUrl: string
  pexelsUrl: string
}

export interface AudioResolution {
  audio_url: string | null
  audio_source: 'dictionaryapi.dev' | 'tts' | 'none'
}

export interface ImageResolution {
  imagen_url: string
  image_source: 'custom' | 'pexels' | 'picsum' | 'svg'
}

export interface VerbEnrichment {
  imagen_url: string
  image_source: ImageResolution['image_source']
  audio_url: string | null
  audio_source: AudioResolution['audio_source']
}
