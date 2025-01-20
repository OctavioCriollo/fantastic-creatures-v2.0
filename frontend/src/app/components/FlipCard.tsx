"use client"

import type React from "react"
import { useState, useEffect } from "react"
import Image from "next/image"
import { Box, Typography } from "@mui/material"

interface FlipCardProps {
  imageUrl: string
  description: string
  isFlipped: boolean
  onClick: () => void
}

export const FlipCard: React.FC<FlipCardProps> = ({ imageUrl, description, isFlipped, onClick }) => {
  const [currentHeight, setCurrentHeight] = useState<number>(0)

  useEffect(() => {
    const updateDimensions = () => {
      const windowWidth = window.innerWidth

      if (isFlipped) {
        const txtElement = document.getElementById("creature-description")
        const txtHeight = txtElement?.offsetHeight || windowWidth
        setCurrentHeight(Math.max(txtHeight, 400))
      } else {
        setCurrentHeight(windowWidth)
      }
    }

    updateDimensions()
    window.addEventListener("resize", updateDimensions)
    return () => window.removeEventListener("resize", updateDimensions)
  }, [isFlipped])

  return (
    <Box
      className={`flip-card ${isFlipped ? "flipped" : ""}`}
      onClick={onClick}
      sx={{
        width: "100vw",
        height: `${currentHeight}px`,
        position: "relative",
        perspective: "1000px",
        transition: "height 0.6s ease-in-out",
        display: "flex",
        justifyContent: "center",
      }}
    >
      <Box
        className="flip-card-inner"
        sx={{
          position: "relative",
          width: "calc(100% - 32px)",
          maxWidth: "calc(100vw - 32px)",
          height: "100%",
          transition: "transform 0.6s",
          transformStyle: "preserve-3d",
          transform: isFlipped ? "rotateY(180deg)" : "rotateY(0deg)",
        }}
      >
        {/* Frente - Imagen */}
        <Box
          className="flip-card-front"
          sx={{
            position: "absolute",
            width: "100%",
            height: "100%",
            backfaceVisibility: "hidden",
            WebkitBackfaceVisibility: "hidden",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            borderRadius: "20px", // Bordes redondeados para el contenedor frontal
            overflow: "hidden", // Para asegurar que la imagen respete los bordes
          }}
        >
          <Box
            sx={{
              position: "relative",
              width: "100%",
              height: "100%",
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <Image
              id="creature-image"
              src={imageUrl || "/placeholder.svg"}
              alt="Creature"
              fill
              sizes="100vw"
              style={{
                objectFit: "contain",
                borderRadius: "20px", // Bordes redondeados para la imagen
              }}
              priority
            />
          </Box>
        </Box>

        {/* Reverso - Descripción */}
        <Box
          className="flip-card-back"
          sx={{
            position: "absolute",
            width: "100%",
            height: "100%",
            bgcolor: "rgba(0,0,0,0.8)",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            px: 2,
            backfaceVisibility: "hidden",
            WebkitBackfaceVisibility: "hidden",
            transform: "rotateY(180deg)",
            borderRadius: "20px", // Bordes redondeados para el contenedor con sombreado
          }}
        >
          <Box
            sx={{
              width: "100%",
              height: "100%",
              display: "flex",
              alignItems: "center",
            }}
          >
            <Typography
              id="creature-description"
              sx={{
                color: "#fff",
                fontSize: "16px",
                lineHeight: 1.8,
                textAlign: "justify",
                width: "100%",
                marginTop: "48px",
                marginBottom: "48px",
                paddingTop: "24px",
                paddingBottom: "24px",
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

