"use client"

//import React, { useState, useCallback, useMemo } from "react"
import React, { useState, useCallback, useMemo, useRef, useEffect } from "react" // Modificado

import { generateCreature, buyCreature } from "@/api/api"
import { ClipLoader } from "react-spinners"
import { Button, TextField, Typography, Container, Box, Alert, Stack } from "@mui/material"
import Image from "next/image"
import { createTheme, ThemeProvider } from "@mui/material/styles"
import { FlipCard } from "./components/FlipCard"

interface Creature {
  name: string
  image_url: string
  description: string
  unique_number: string
}

interface ApiResponse {
  message: string
  QR_code_url?: string
}

const PAYMENT_AMOUNT = 199
const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL

const buildUrl = (path: string) => {
  const base = API_URL?.endsWith('/api') 
    ? API_URL 
    : `${API_URL}/api`;
    
  return `${base.replace(/\/$/, '')}/${path.replace(/^\//, '')}`;
}

const HomePage = () => {
  const [generateMessage, setGenerateMessage] = useState<string>("")
  const [donateMessage, setDonateMessage] = useState<string>("")
  const [clientName, setClientName] = useState<string>("")
  const [birthDate, setBirthDate] = useState<string>("")
  const [creatureDetails, setCreatureDetails] = useState<string>("")
  const [creature, setCreature] = useState<Creature | null>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [buyingLoading, setBuyingLoading] = useState<boolean>(false)
  const [qrCodeUrl, setQrCodeUrl] = useState<string>("")
  const [showDescription, setShowDescription] = useState<boolean>(false)

  const [isDateFocused, setIsDateFocused] = useState<boolean>(false) 
  const creatureRef = useRef<HTMLDivElement>(null) // Nueva referencia

  useEffect(() => {
    if (creature && creatureRef.current) {
      creatureRef.current.scrollIntoView({
        behavior: "smooth",
        block: "start"
      })
    }
  }, [creature])  

  const theme = useMemo(() => createTheme({
    breakpoints: {
      values: {
        xs: 0,
        sm: 480,
        md: 900,
        lg: 1200,
        xl: 1536,
      },
    },
  }), [])

  const handleError = (error: unknown): string => {
    if (error instanceof Error) return error.message
    return typeof error === 'object' && error !== null && 'message' in error 
      ? String(error.message) 
      : "Error desconocido"
  }

  const resetState = () => {
    setGenerateMessage("")
    setDonateMessage("")
    setCreature(null)
    setShowDescription(false)
    setQrCodeUrl("")
  }

  const isValidDate = (date: string) => !isNaN(Date.parse(date))

  const handleBuyCreature = useCallback(async () => {
    if (!creature) {
      setDonateMessage("Please generate a creature first.")
      return
    }
    
    setBuyingLoading(true)
    try {
      const data = await buyCreature(clientName, "", birthDate, creature) as ApiResponse
      setDonateMessage(data.message)
      setQrCodeUrl(data.QR_code_url || "")
    } catch (error) {
      setDonateMessage(handleError(error))
    } finally {
      setBuyingLoading(false)
    }
  }, [clientName, birthDate, creature])

  const handleGenerateCreature = async () => {
    if (!clientName) return setGenerateMessage("Se requiere el nombre.")
    if (!birthDate) return setGenerateMessage("Se requiere la fecha de nacimiento.")
    if (!creatureDetails) return setGenerateMessage("Se requieren los detalles de la criatura.")
    if (!isValidDate(birthDate)) return setGenerateMessage("Fecha inválida")

    resetState()
    setLoading(true)

    try {
      const data = await generateCreature(clientName, birthDate, "", creatureDetails)
      setCreature(data)
    } catch (error) {
      setGenerateMessage(handleError(error))
    } finally {
      setLoading(false)
    }
  }

  const toggleDescription = () => setShowDescription(!showDescription)

 
  const PurchaseSection = () => (
    <Box sx={{
      width: "100%",
      bgcolor: "rgba(0, 0, 0, 0.3)",
      mt: 2,
      py: 3,
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
    }}>
      <Button
        variant="contained"
        onClick={handleBuyCreature}
        disabled={buyingLoading}
        sx={{
          bgcolor: "#CC24DE !important", // Color base
          color: "white !important",
          px: 4,
          py: 1.2,
          fontSize: "1rem",
          fontWeight: 600,
          transition: "all 0.3s ease",
          "&:hover": {
            bgcolor: "#B020BE !important", // Hover: +10% oscuro
            transform: "scale(1.02)"
          },
          "&:active": {
            bgcolor: "#6A1B9A !important", // Active: Mismo color base
            transform: "scale(0.98)", // Efecto de presión
            boxShadow: "0 2px 4px rgba(0,0,0,0.2)"
          },
          "&.Mui-disabled": {
            bgcolor: "#B020BE !important",
            opacity: 0.7,
            transform: "none"
          }
        }}
        
        //sx={{
        //  bgcolor: "#CC24DE",
        //  "&:hover": { bgcolor: "#B020BE" },
        //  px: 4,
        //  py: 1.2,
        //  fontSize: "1rem",
        //  fontWeight: 600,
        //}}
        aria-label="Donar"
        aria-busy={buyingLoading}
      >
        {buyingLoading ? (
          <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
            <ClipLoader color="#ffffff" size={20} />
            Processing...
          </Box>
        ) : "Donate"}
      </Button>
      
      <Typography variant="h6" sx={{ color: "white", mb: 0, mt: 2 }}>
        Share or Donate
      </Typography>
      <Typography sx={{ color: "#ddd", mb: 0 }}>
        from ${PAYMENT_AMOUNT / 100} USD
      </Typography>
      
      {donateMessage && (
        <Box sx={{ mt: 2, mb: 0, width: "auto", textAlign: "center" }}>
          <Alert severity={donateMessage.includes("error") ? "error" : "success"}>
            {donateMessage}
          </Alert>
        </Box>
      )}
    </Box>
  )

  return (
    <ThemeProvider theme={theme}>
      <Container
        maxWidth={false}
        disableGutters
        sx={{
          //maxWidth: "760px",
          minHeight: "100svh",
          height: "auto",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "flex-start",
          overflow: "hidden",
          pt: 4
        }}
      >
        {/* Header */}
        <Box sx={{ maxWidth: "100%", width: "100%", mb: 2, px: 2 }}>
            <Typography variant="h4" align="center" sx={{
              fontSize: "24px",
              fontWeight: 700,
              color: "#FFFFFF",
              mb: 1,
            }}>
              FANTASTIC CREATURES
            </Typography>
            
            <Typography variant="body2" align="center" sx={{
              color: "#B0BEC5",
              fontSize: "14px",
              mb: "5px",
            }}>
              Crea tu criatura mágica y mitológica basado en tu fecha de nacimiento y tu nombre. Ingresa abajo.
            </Typography>
        </Box>

        {/* Form Section */}
        <Box sx={{ maxWidth: "100%", width: "100%", mb: 4, px: 2 }}>
          <Stack spacing={2} width="100%">
            <Box display="flex" flexDirection={["column", "row"]} gap={2}>
              {/* Full Name TextField */}
              <TextField
                fullWidth
                placeholder="Full Name"
                value={clientName}
                onChange={(e) => setClientName(e.target.value)}
                variant="filled"
                InputProps={{
                  disableUnderline: true,
                  sx: {
                    borderRadius: "8px",
                    backgroundColor: "white",
                    "&:hover": { backgroundColor: "white" },
                    "&.Mui-focused": { backgroundColor: "white" },
                    "& input": {
                      color: "#000000DE !important",
                      padding: "10px 14px",
                      "&::placeholder": {
                        opacity: 0.7,
                        color: "rgba(0, 0, 0, 0.6) !important"
                      }
                    }
                  }
                }}
              />
              {/* Date of Birth TextField */}
              <TextField
                fullWidth
                type="date"
                value={birthDate}
                onChange={(e) => setBirthDate(e.target.value)}
                onFocus={() => setIsDateFocused(true)}
                onBlur={() => setIsDateFocused(false)}
                variant="filled"
                InputLabelProps={{
                  shrink: true,
                  sx: {
                    color: "rgba(0, 0, 0, 0.6)",
                    opacity: 0.7,
                    fontSize: "16px",
                    marginBottom: "8px",
                    // Eliminar transformaciones forzadas
                    transform: "none",
                    position: "relative",
                  }
                }}
                InputProps={{
                  disableUnderline: true,
                  sx: {
                    borderRadius: "8px",
                    bgcolor: "white",
                    "&:hover, &.Mui-focused": {
                      bgcolor: "white !important"
                    },
                    "& input": {
                      padding: "10px 14px !important",
                      position: "relative",
                      zIndex: 1,
                      "&::-webkit-datetime-edit": {
                        color: isDateFocused || birthDate ? "inherit" : "transparent !important",
                      },
                      "&::-webkit-calendar-picker-indicator": {
                        color: "rgba(0, 0, 0, 0.54) !important",
                        zIndex: 2
                      },
                    },
                    "&::before": {
                      content: '"Date of Birth"',
                      position: "absolute",
                      left: "14px",
                      top: "50%",
                      transform: "translateY(-50%)",
                      color: "rgba(0, 0, 0, 0.6) !important",
                      opacity: (isDateFocused || birthDate) ? 0 : 0.7,
                      pointerEvents: "none",
                      transition: "opacity 0.2s",
                      zIndex: 1
                    },
                  }
                }}
              />
            </Box>
            
            {/* Define Your Creature TextField */}
            <TextField
              fullWidth
              placeholder="Define Your Creature"
              value={creatureDetails}
              onChange={(e) => setCreatureDetails(e.target.value)}
              variant="filled"
              InputProps={{
                disableUnderline: true,
                sx: {
                  borderRadius: "8px",
                  backgroundColor: "white",
                  "&:hover": { backgroundColor: "white" },
                  "&.Mui-focused": { backgroundColor: "white" },
                  "& input": {
                    color: "#000000DE !important",
                    padding: "16px 14px",
                    "&::placeholder": {
                      opacity: 0.7,
                      color: "rgba(0, 0, 0, 0.6) !important"
                    }
                  }
                }
              }}
            />
          </Stack>
          
          <Box sx={{ display: "flex", justifyContent: "center", mt: 4 }}>
            <Button
              variant="contained"
              onClick={handleGenerateCreature}
              disabled={loading}
              sx={{
                bgcolor: "#00C3F3",
                color: "white",
                px: 4,
                py: 1.5,
                "&:hover": { bgcolor: "#00B3E3" },
                "&.Mui-disabled": { bgcolor: "#00C3F3", opacity: 0.7 },
              }}
              aria-label="Generar criatura"
              aria-busy={loading}
            >
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                {loading && <ClipLoader color="#ffffff" size={20} />}
                {loading ? "GENERANDO..." : "GENERATE CREATURE"}
              </Box>
            </Button>
          </Box>

          {generateMessage && (
            <Box sx={{ mt: 3, display: "flex", justifyContent: "center", width: "100%" }}>
              <Alert 
                severity={generateMessage.includes("error") ? "error" : "warning"} 
                sx={{ maxWidth: "100%", padding: "8px 16px" }}
              >
                {generateMessage}
              </Alert>
            </Box>
          )}
        </Box>
      

        {/* Loading State */}
        {loading && (
          <Box sx={{ height: 300, display: 'grid', placeItems: 'center' }}>
            <ClipLoader color="#FF4245" size={100} />
            <Typography sx={{ color: "#fff", mt: 2 }}>Creando tu Criatura...</Typography>
          </Box>
        )}

        {/* Creature Display */}
        {!loading && creature && (
          <Box 
            ref={creatureRef}  // Agregar referencia aquí
            sx={{ width: "100%", mt: "0px", display: "flex", flexDirection: "column", alignItems: "center" }}>
                          
            <Typography variant="h5" align="center" sx={{
              color: "white",
              textTransform: "uppercase",
              fontWeight: 700,
              mb: 0.5,
              px: 2,
            }}>
              {creature.name}
            </Typography>
            
            <Typography sx={{ color: "white", mb: 0, textAlign: "center" }}>
              <strong>Creature Number:</strong> {creature.unique_number}
            </Typography>
            
            <Typography sx={{
              color: "rgba(255, 255, 255, 0.5)",
              mt: 1,
              mb: 0,
              textAlign: "center",
              cursor: "pointer",
            }} onClick={toggleDescription}>
              Click para {showDescription ? "ver la imagen" : "ver la descripción"}
            </Typography>

            {/* Flip Card Container */}
            <Box sx={{
              width: "100vw",
              display: "flex",
              justifyContent: "center",
              margin: 0,
              padding: 0,
              left: "50%",
              position: "relative",
              transform: "translateX(-50%)",
              mt: 1,
              
            


            }}>
              <FlipCard
                imageUrl={buildUrl(creature.image_url)}
                description={creature.description}
                isFlipped={showDescription}
                onClick={toggleDescription}
              />
            </Box>
            <PurchaseSection />
          </Box>
        )}

        {/* QR Code Display */}
        {qrCodeUrl && (
          <Box sx={{ mt: 2, textAlign: "center", px: 2 }}>
            <Typography variant="h6" sx={{ color: "white", mb: 2 }}>
              Your QR Code
            </Typography>
            <Image
              src={qrCodeUrl}
              alt="Creature QR Code"
              width={200}
              height={200}
              style={{ margin: "0 auto" }}
            />
            <Typography sx={{ color: "#ddd", mt: 2 }}>
              {buildUrl(qrCodeUrl)}
            </Typography>
          </Box>
        )}
      </Container>
    </ThemeProvider>
  )
}

export default HomePage