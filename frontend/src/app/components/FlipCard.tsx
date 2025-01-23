"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { Box, Typography, CircularProgress } from "@mui/material"
import { SxProps } from "@mui/material/styles";


interface FlipCardProps {
  imageUrl: string
  description: string
  isFlipped: boolean
  onClick: () => void
  sx?: SxProps;
}

export const FlipCard: React.FC<FlipCardProps> = ({ imageUrl, description, isFlipped, onClick }) => {
  const [currentHeight, setCurrentHeight] = useState<number>(400)
  const [imgStatus, setImgStatus] = useState<"loading" | "loaded" | "error">("loading")

  // Función debounce mejorada
  function debounce<T extends (...args: unknown[]) => void>(fn: T, delay: number) {
    let timeoutId: NodeJS.Timeout
    return (...args: Parameters<T>) => {
      clearTimeout(timeoutId)
      timeoutId = setTimeout(() => fn(...args), delay)
    }
  }

  // Cálculo preciso de altura
  useEffect(() => {
    const calculateHeight = () => {
      if (isFlipped) {
        const txtElement = document.getElementById("creature-description")
        if (!txtElement) return 400

        const computedStyle = window.getComputedStyle(txtElement)
        const paddingTop = parseFloat(computedStyle.paddingTop)
        const paddingBottom = parseFloat(computedStyle.paddingBottom)
        
        return Math.ceil(txtElement.scrollHeight + paddingTop + paddingBottom)
      }
      return Math.min(window.innerWidth * 0.9, window.innerHeight * 0.6)
    }

    const updateDimensions = () => setCurrentHeight(calculateHeight())
    
    updateDimensions()
    const debouncedUpdate = debounce(updateDimensions, 50)
    window.addEventListener("resize", debouncedUpdate)
    
    return () => window.removeEventListener("resize", debouncedUpdate)
  }, [isFlipped, description])

  return (
    <Box
      role="button"
      aria-label={isFlipped ? "Ver imagen" : "Ver descripción"}
      tabIndex={0}
      onKeyDown={(e) => e.key === "Enter" && onClick()}
      onClick={onClick}
      sx={{
        width: "100vw",
        height: `${currentHeight}px`,
        position: "relative",
        perspective: "1000px",
        transition: "height 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        display: "flex",
        justifyContent: "center",
        margin: "0 auto",
        maxWidth: "1200px",
        cursor: "pointer",
        overflow: "hidden"
      }}
    >
      <Box
        sx={{
          position: "relative",
          width: "calc(100% - 32px)",
          maxWidth: "calc(100vw - 32px)",
          height: "100%",
          transition: "transform 0.6s cubic-bezier(0.4, 0, 0.2, 1)",
          transformStyle: "preserve-3d",
          willChange: "transform",
          transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)",
        }}
      >
        {/* Frente - Imagen */}
        <Box
          sx={{
            position: "absolute",
            width: "100%",
            height: "100%",
            backfaceVisibility: "hidden",
            WebkitBackfaceVisibility: "hidden",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            borderRadius: "20px",
            overflow: "hidden",
            //bgcolor: "rgba(0,0,0,0.1)"
          }}
        >
          <Box sx={{ 
            position: "relative", 
            width: "100%", 
            height: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center"
          }}>
            <Image
              id="creature-image"
              src={imageUrl}
              alt="Creature"
              fill
              sizes="100vw"
              //sizes="(max-width: 768px) 100vw, 50vw"
              priority
              onLoadingComplete={() => setImgStatus("loaded")}
              onError={() => setImgStatus("error")}
              style={{
                objectFit: "cover",
                borderRadius: "20px",
                display: imgStatus === "loaded" ? "block" : "none",
              }}
            />
          </Box>

          {imgStatus === "loading" && (
            <Box sx={{ 
              position: "absolute", 
              display: "flex", 
              gap: 2, 
              alignItems: "center",
              flexDirection: 'column',
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              justifyContent: "center",
              backgroundColor: "rgba(0, 0, 0, 0.5)",
              overflow: "hidden"
            }}>
              <CircularProgress color="secondary" />
              <Typography variant="body2" sx={{ color: "white" }}>
                Cargando imagen...
              </Typography>
            </Box>
          )}

          {imgStatus === "error" && (
            <Box sx={{ 
              position: "absolute",
              width: "100%",
              height: "100%",
              display: "flex",
              flexDirection: "column",
              justifyContent: "center",
              alignItems: "center",
              backgroundColor: "rgba(0, 0, 0, 0.7)"
            }}>
              <Typography variant="h6" color="error">
                Error cargando la imagen
              </Typography>
              <Typography variant="body2" sx={{ mt: 1, color: "white" }}>
                Intenta recargar la página
              </Typography>
            </Box>
          )}
        </Box>

        {/* Reverso - Descripción */}
        <Box
          sx={{
            position: "absolute",
            width: "100%",
            height: "100%",
            bgcolor: "rgba(0,0,0,0.85)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            px: 2,
            backfaceVisibility: "hidden",
            WebkitBackfaceVisibility: "hidden",
            transform: "rotateY(180deg)",
            borderRadius: "20px",
            //overflow: "hidden",
            //boxSizing: "border-box"
          }}
        >
          <Box
            sx={{
              width: "100%",
              height: "100%",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              //padding: "32px",
              //boxSizing: "border-box"
            }}
          >
            <Typography
              id="creature-description"
              sx={{
                color: "#fff",
                fontSize: "16px",
                //fontSize: "clamp(14px, 2vw, 18px)",
                lineHeight: 1.8,
                textAlign: "justify",
                textJustify: "inter-word",
                hyphens: "auto",
                
                whiteSpace: "pre-wrap",
                wordWrap: "break-word",
                overflowWrap: "break-word",
                wordBreak: "break-word",
                display: "block",
                padding: "2px",

                maxWidth: "100%",
                width: "100%",
                height: "auto",
                overflow: "hidden",
                
                marginTop: "48px",
                marginBottom: "48px",
                paddingTop: "16px",
                paddingBottom: "16px"

              }}
            >
              {description}
            </Typography>
          </Box>
        </Box>
      </Box>
    </Box>
  )
}