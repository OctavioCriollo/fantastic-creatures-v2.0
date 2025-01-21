"use client"

import React, { useState, useCallback } from "react"
import { generateCreature, buyCreature } from "@/api/api"
import { ClipLoader } from "react-spinners"
import { Button, TextField, Typography, Container, Box, Alert, Stack } from "@mui/material"
import Image from "next/image"
import { createTheme, ThemeProvider } from "@mui/material/styles"
import { FlipCard } from "./components/FlipCard"

const theme = createTheme({
  breakpoints: {
    values: {
      xs: 0,
      sm: 480,
      md: 900,
      lg: 1200,
      xl: 1536,
    },
  },
})

interface Creature {
  name: string
  image_url: string
  description: string
  unique_number: string
}

const PAYMENT_AMOUNT = 199
const API_URL = process.env.NEXT_PUBLIC_BACKEND_API_URL

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
  const [isDateFocused, setIsDateFocused] = useState(false)

  const handleBuyCreature = useCallback(async () => {
    if (!creature) {
      setDonateMessage("Please generate a creature first.")
      return
    }
    setBuyingLoading(true)
    try {
      const data = await buyCreature(clientName, "", birthDate, creature)
      setDonateMessage(data.message)
      setQrCodeUrl(data.QR_code_url)
    } catch (error: unknown) {
      if (error instanceof Error) {
        setDonateMessage(error.message)
      } else {
        setDonateMessage("An unexpected error occurred.")
      }
    } finally {
      setBuyingLoading(false)
    }
  }, [clientName, birthDate, creature])

  const handleGenerateCreature = async () => {
    if (!clientName) {
      setGenerateMessage("Se requiere el nombre.")
      return
    }

    if (!birthDate) {
      setGenerateMessage("Se requiere la fecha de nacimiento.")
      return
    }

    if (!creatureDetails) {
      setGenerateMessage("Se requieren los detalles de la criatura.")
      return
    }

    setGenerateMessage("")
    setDonateMessage("")
    // Clear existing creature data
    setCreature(null)
    setShowDescription(false)
    setQrCodeUrl("")
    setLoading(true)

    try {
      const data = await generateCreature(clientName, birthDate, "", creatureDetails)
      setCreature(data)
    } catch (error: unknown) {
      if (error instanceof Error) {
        setGenerateMessage(error.message)
      } else {
        setGenerateMessage("An unexpected error occurred while generating the creature.")
      }
    } finally {
      setLoading(false)
    }
  }

  const toggleDescription = () => {
    setShowDescription(!showDescription)
  }

  return (
    <ThemeProvider theme={theme}>
      <Container
        maxWidth={false}
        disableGutters
        sx={{
          background: "linear-gradient(180deg, #0D3F4D 0%, #0A2F3A 100%)",
          minHeight: "100vh",
          height: "100vh",
          //minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          //justifyContent: "flex-start",
          pt: 4,
        }}
      >
        {/* Header Section */}
        <Box sx={{ maxWidth: "800px", width: "100%", mb: 2, px: 2 }}>
          <Typography
            variant="h4"
            align="center"
            sx={{
              fontSize: "24px",
              fontWeight: 700,
              color: "#FFFFFF",
              mb: 1,
            }}
          >
            FANTASTIC CREATURES
          </Typography>
          <Typography
            variant="body2"
            align="center"
            sx={{
              color: "#B0BEC5",
              fontSize: "14px",
              mb: "5px",
            }}
          >
            Crea tu criatura mágica y mitológica basado en tu fecha de nacimiento y tu nombre. Ingresa abajo.
          </Typography>
        </Box>

        {/* Form Section */}
        <Box sx={{ maxWidth: "800px", width: "100%", mb: 4, px: 2 }}>
          <Stack spacing={2} width="100%">
            <Box display="flex" flexDirection={["column", "row"]} gap={2}>
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
                    bgcolor: "white",
                    "&:hover": { bgcolor: "white" },
                    "&.Mui-focused": { bgcolor: "white" },
                    "& input": {
                      padding: "10px 14px",
                    },
                    "& input::placeholder": {
                      opacity: 0.7,
                      color: "rgba(0, 0, 0, 0.6)",
                    },
                  },
                }}
              />
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
                    position: "relative",
                    transform: "none",
                    fontSize: "16px",
                    marginBottom: "8px",
                  },
                }}
                InputProps={{
                  disableUnderline: true,
                  sx: {
                    borderRadius: "8px",
                    bgcolor: "white",
                    "&:hover": { bgcolor: "white" },
                    "&.Mui-focused": { bgcolor: "white" },
                    "& input": {
                      padding: "10px 14px",
                      "&::-webkit-datetime-edit": {
                        color: isDateFocused || birthDate ? "inherit" : "transparent",
                      },
                      "&::-webkit-calendar-picker-indicator": {
                        color: "rgba(0, 0, 0, 0.54)",
                      },
                    },
                    "&::before": {
                      content: '"Date of Birth"',
                      position: "absolute",
                      left: "14px",
                      top: "50%",
                      transform: "translateY(-50%)",
                      color: "rgba(0, 0, 0, 0.6)",
                      opacity: 0.7,
                      pointerEvents: "none",
                      transition: "opacity 0.2s",
                      display: isDateFocused || birthDate ? "none" : "block",
                    },
                  },
                }}
              />
            </Box>
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
                  bgcolor: "white",
                  "&:hover": { bgcolor: "white" },
                  "&.Mui-focused": { bgcolor: "white" },
                  "& input": {
                    padding: "16px 14px",
                  },
                  "& input::placeholder": {
                    opacity: 0.7,
                    color: "rgba(0, 0, 0, 0.6)",
                  },
                },
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
                "&:hover": {
                  bgcolor: "#00B3E3",
                },
                "&.Mui-disabled": {
                  bgcolor: "#00C3F3",
                  opacity: 0.7,
                  color: "white",
                },
              }}
            >
              <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                {loading && <ClipLoader color="#ffffff" size={20} />}
                {loading ? "GENERATING..." : "GENERATE CREATURE"}
              </Box>
            </Button>
          </Box>
          
        

          {generateMessage && (
            <Box sx={{ mt: 3, display: "flex", justifyContent: "center", width: "100%" }}>
              <Alert 
                severity={generateMessage.includes("error") ? "error" : "warning"} 
                sx={{ display: "flex", textAlign: "center", maxWidth: "100%", padding: "8px 16px" }}
              >
                {generateMessage}
              </Alert>
            </Box>
          )}

        </Box>

        {loading && (
          <Box sx={{ textAlign: "center", my: 4 }}>
            <ClipLoader color="#FF4245" size={100} />
            <Typography sx={{ color: "#fff", mt: 2 }}>Creando tu Criatura...</Typography>
          </Box>
        )}

        {/* Creature Section - Modified for full width and proper background colors */}
        {!loading && creature && (
          <Box
            sx={{
              width: "100%",
              mt: "0px",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
            }}
          >
            <Typography
              variant="h5"
              align="center"
              sx={{
                color: "white",
                textTransform: "uppercase",
                fontWeight: 700,
                mb: 0.5,
                px: 2,
              }}
            >
              {creature.name}
            </Typography>
            <Typography
              sx={{
                color: "white",
                mb: 0,
                textAlign: "center",
              }}
            >
              <strong>Creature Number:</strong> {creature.unique_number}
            </Typography>
            <Typography
              sx={{
                color: "rgba(255, 255, 255, 0.5)",
                mt: 1,
                mb: 0,
                textAlign: "center",
                cursor: "pointer",
              }}
              onClick={toggleDescription}
            >
              Click para {showDescription ? "ver la imagen" : "ver la descripción"}
            </Typography>

            {/* Full width container for FlipCard */}
            <Box
              sx={{
                width: "100vw",
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                margin: 0,
                padding: 0,
                left: "50%",
                position: "relative",
                transform: "translateX(-50%)",
                mt: 1,
              }}
            >
              <FlipCard
                imageUrl={`${API_URL}/api/${creature.image_url}`}
                description={creature.description}
                isFlipped={showDescription}
                onClick={toggleDescription}
              />
            </Box>

            {/* Purchase section with darker background */}
            <Box
              sx={{
                width: "100%",
                bgcolor: "rgba(0, 0, 0, 0.3)",
                mt: 4,
                py: 4,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              <Box sx={{ textAlign: "center", mb: 0, mt: 1 }}>         
                <Button
                  variant="contained"
                  onClick={handleBuyCreature}
                  disabled={buyingLoading}
                  sx={{
                    bgcolor: "#CC24DE",
                    "&:hover": { bgcolor: "#B020BE" },
                    px: 4,
                    py: 1.2,
                    fontSize: "1rem",
                    fontWeight: 600,
                  }}
                >
                  {buyingLoading ? (
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <ClipLoader color="#ffffff" size={20} />
                      Processing...
                    </Box>
                  ) : (
                    "Donate"
                  )}
                </Button>
                <Typography variant="h6" sx={{ color: "white", mb: 0, mt: 2 }}>
                  Share or Donate
                </Typography>
                <Typography sx={{ color: "#ddd", mb: 0 }}>from ${PAYMENT_AMOUNT / 100} USD</Typography>
                {donateMessage && (
                  <Box sx={{ mt: 0, mb: 0, width: "auto", textAlign: "center" }}>
                    <Alert severity={donateMessage.includes("error") ? "error" : "success"}>{donateMessage}</Alert>
                  </Box>
                )}
              </Box>
            </Box>
          </Box>
        )}

        {qrCodeUrl && (
          <Box sx={{ mt: 4, textAlign: "center", px: 2 }}>
            <Typography variant="h6" sx={{ color: "white", mb: 2 }}>
              Your QR Code
            </Typography>
            <Image
              src={qrCodeUrl || "/placeholder.svg"}
              alt="Creature QR Code"
              width={200}
              height={200}
              style={{ margin: "0 auto" }}
            />
            <Typography sx={{ color: "#ddd", mt: 2 }}>{`${API_URL}${qrCodeUrl}`}</Typography>
          </Box>
        )} 
      </Container>
    </ThemeProvider>
  )
}

export default HomePage

